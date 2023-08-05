import peewee
import re


class undo:
    active = 0
    first_log = 1
    frozen = -1

    undo_stack = None
    redo_stack = None

    next_text = ""

    def __init__(self, db, tables):
        # store the database and the tables
        self.db = db
        self.tables = tables

    def activate(self):
        """
        Start up the undo/redo system
        """
        # already active? do nothing
        if self.active:
            return
        # create the triggers to log changes
        self._create_triggers()
        # initialize the stacks
        self.undo_stack = []
        self.redo_stack = []
        # initialize the variables
        self.active = 1
        self.frozen = -1
        # start the first undo interval
        self._start_interval()

    def deactivate(self):
        """
        Halt the undo/redo system and delete the undo/redo stacks
        """
        # not active? do nothing
        if not self.active:
            return
        # delete the triggers from the database
        self._drop_triggers()
        # remove the stacks
        self.undo_stack = None
        self.redo_stack = None
        # reset the variables
        self.active = 0
        self.frozen = -1

    def freeze(self):
        """
        Stop accepting database changes into the undo stack

        From the point when this routine is called up until the next unfreeze,
        new database changes are rejected from the undo stack.
        """
        # if the recording is frozen, do nothing
        if self.frozen >= 0:
            return
        # get the current index from the undo log
        self.frozen = self._get_last_index()

    def unfreeze(self):
        """
        Begin accepting undo actions again.
        """
        # if the recording is not frozen, do nothing
        if self.frozen < 0:
            return
        # delete the recorded changes during the frozen period
        self.db.execute_sql("DELETE FROM undolog WHERE seq > ?", (self.frozen, ))
        # reset the frozen variable
        self.frozen = -1

    def barrier(self, text=""):
        """
        Create an undo barrier right now.
        """
        # get the index of the last recorded change
        end = self._get_last_index()
        # if there were some changes recorded during the freezing, omit those
        if 0 <= self.frozen < end:
            end = self.frozen
        # the beginning is the stored first index
        begin = self.first_log
        # start a new undo interval
        self._start_interval()
        # if the beginning of the undo is the same as the current index, no changes occurred since the last barrier
        if begin == self.first_log:
            self.refresh()
            return
        # add the interval to the undo stack, together with the optional descriptive text
        self.undo_stack.append((begin, end, text))
        # delete the redo stack
        self.redo_stack = []
        # refresh the gui
        self.refresh()

    def __call__(self, text=""):
        self.next_text = text
        return self

    def __enter__(self):
        """
        Enter an undo context where every changes is gathered into an undo interval
        """
        #self.unfreeze()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit an undo context and an undo barrier
        """
        self.barrier(self.next_text)
        self.next_text = ""
        #self.freeze()

    def undo(self):
        """
        Do a single step of undo
        """
        self._step(self.undo_stack, self.redo_stack)

    def redo(self):
        """
        Redo a single step
        """
        self._step(self.redo_stack, self.undo_stack)

    def get_state(self):
        """
        Get the text for the last undo and redo command, or None if it is not available
        """
        try:
            undo = self.undo_stack[-1][2]
        except IndexError:
            undo = None

        try:
            redo = self.redo_stack[-1][2]
        except IndexError:
            redo = None
        return undo, redo

    def refresh(self):
        """
        Update the status of controls after a database change

        The undo module calls this routine after any undo/redo in order to
        cause controls gray out appropriately depending on the current state
        of the database. This routine works by invoking the status_refresh
        module in all top-level namespaces.
        """
        pass

    def reload_all(self):
        """
        Redraw everything based on the current database

        The undo module calls this routine after any undo/redo in order to
        cause the screen to be completely redrawn based on the current database
        contents. This is accomplished by calling the "reload" module in
        every top-level namespace other than ::undo.
        """
        pass

    def status_refresh(self):
        """
        Enable and/or disable menu options a buttons
        """
        pass

    def _create_triggers(self):
        """
        Create change recording triggers for all tables listed

        Create a temporary table in the database named "undolog". Create triggers that fire on any insert, delete, or
        update of TABLE1, TABLE2, .... When those triggers fire, insert records in undolog that contain SQL text for
        statements that will undo the insert, delete, or update.
        """
        # delete a potential previous undo log table
        try:
            self.db.execute_sql('DROP TABLE undolog')
        except peewee.OperationalError:
            pass
        # create a new undo log table
        self.db.execute_sql('CREATE TEMP TABLE undolog(seq integer primary key, sql text)')

        # iterate over the tables to track
        for tbl in self.tables:
            # get a list of all columns
            collist = self.db.execute_sql('pragma table_info({tbl})'.format(tbl=tbl)).fetchall()

            # create a trigger for insert commands on the table
            sql = "CREATE TEMP TRIGGER _{tbl}_it AFTER INSERT ON {tbl} BEGIN\n"
            sql += "  INSERT INTO undolog VALUES(NULL,"
            sql += "'DELETE FROM {tbl} WHERE rowid='||new.rowid);\nEND\n"
            # add the trigger
            self.db.execute_sql(sql.format(tbl=tbl))

            # create a trigger for update commands on the table
            sql = "CREATE TEMP TRIGGER _{tbl}_ut AFTER UPDATE ON {tbl} BEGIN\n"
            sql += "  INSERT INTO undolog VALUES(NULL,"
            sql += "'UPDATE {tbl} "
            # add a set with the old values
            sep = "SET "
            for x1, name, x2, x3, x4, x5 in collist:
                sql += "{sep}{name}='||quote(old.{name})||'".format(sep=sep, name=name)
                sep = ","
            sql += " WHERE rowid='||old.rowid);\nEND\n"
            # add the trigger
            self.db.execute_sql(sql.format(tbl=tbl))

            # create a trigger for delete commands on the table
            sql = "CREATE TEMP TRIGGER _{tbl}_dt BEFORE DELETE ON {tbl} BEGIN\n"
            sql += "  INSERT INTO undolog VALUES(NULL,"
            sql += "'INSERT INTO {tbl}(rowid"
            # add a set with the old values
            for x1, name, x2, x3, x4, x5 in collist:
                sql += ","+name
            sql += ") VALUES('||old.rowid||'"
            for x1, name, x2, x3, x4, x5 in collist:
                sql += ",'||quote(old.{name})||'".format(name=name)
            sql += ")');\nEND\n"
            # add the trigger
            self.db.execute_sql(sql.format(tbl=tbl))

    def _drop_triggers(self):
        """
        Drop all of the triggers that _create_triggers created.
        """
        # get the list of triggers
        trigger_list = self.db.execute_sql("SELECT name FROM sqlite_temp_master WHERE type='trigger'").fetchall()

        # iterate over all triggers
        for trigger, in trigger_list:
            # if the trigger is named in the form e.g. _marker_it
            if re.match(r"_.*_", trigger):
                # remove the trigger
                self.db.execute_sql("DROP TRIGGER {trigger}".format(trigger=trigger))

        # drop the undo log table
        try:
            self.db.execute_sql('DROP TABLE undolog')
        except peewee.OperationalError:
            pass

    def _start_interval(self):
        """
        Record the starting conditions of an undo interval
        """
        self.first_log = self._get_last_index()+1

    def _step(self, stack_source, stack_target):
        """
        Do a single step of undo or redo

        For an undo stack_source = self.undo_stack and stack_target = self.redo_stack.
        For a redo, stack_source = self.redo_stack and stack_target = self.undo_stack.
        """
        # pop begin and end from the current stack
        begin, end, text = stack_source.pop(-1)

        # get the list of sql commands to revert the action
        sql_list = self.db.execute_sql("SELECT sql FROM undolog WHERE seq>=? AND seq<=? ORDER BY seq DESC", (begin, end)).fetchall()

        # delete these entries from the undo log
        self.db.execute_sql("DELETE FROM undolog WHERE seq>=? AND seq<=?", (begin, end))

        # find the new first entry
        self.first_log = self._get_last_index()+1

        # execute all commands to revert the action
        with self.db.atomic():
            for sql, in sql_list:
                self.db.execute_sql(sql)

        # reload all stuff that depends on the database
        self.reload_all()

        # get the new end and beginning
        end = self._get_last_index()
        begin = self.first_log

        # add them to the other stack
        stack_target.append((begin, end, text))
        # start a new action interval
        self._start_interval()
        # refresh the gui
        self.refresh()

    def _get_last_index(self):
        # get the index of the most recent entry to the undo log
        return self.db.execute_sql("SELECT coalesce(max(seq),0) FROM undolog").fetchone()[0]


if __name__ == "__main__":
    import os
    import sys
    import clickpoints
    import shutil
    import matplotlib.pyplot as plt

    os.chdir(r"D:\Repositories\ClickPointsExamples\TweezerVideos\002")
    try:
        os.remove("test_tmp.cdb-shm")
    except FileNotFoundError:
        pass
    try:
        os.remove("test_tmp.cdb-wal")
    except FileNotFoundError:
        pass
    try:
        os.remove("test_tmp.cdb")
    except FileNotFoundError:
        pass

    shutil.copy("test.cdb", "test_tmp.cdb")
    db = clickpoints.DataFile("test_tmp.cdb")
    ud = undo(db.db, ["marker", "mask"])
    ud.activate()

    print(db.getMarkers().count())
    with ud("add marker"):
        db.setMarkers(frame=0, x=[0, 1], y=[0, 1], type="data")

    with ud("move marker"):
        m = db.getMarker(id=1)
        m.x = 90
        m.save()

    with ud("delete all markers"):
        db.deleteMarkers()

    with ud("add mask"):
        mask = db.getMasks()[0]
        mask.data[:100, :100] = 0
        mask.save()

    plt.subplot(121)
    plt.imshow(db.getMasks()[0].data)

    ud.undo()

    plt.subplot(122)
    plt.imshow(db.getMasks()[0].data)

    plt.show()


