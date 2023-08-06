import random
from datetime import datetime, timedelta

from fasvaorm.models import Base, Vehicle, Drive, Sensor, Unit, Valuetype, Signal, Aggregation, Record, Driver, \
    signal_table_name, Campaign
from fasvaorm.signal import create_signal_table, _TYPE_MIXIN_MAP
from tests.base import EngineTestCase

TEST_VEHICLE = {'serial_number': "ABC", 'dimension_width': 2000, 'dimension_height': 1500, 'dimension_length': 5000}
TEST_DRIVE = {'start': datetime.now(), 'end': datetime.now() + timedelta(seconds=5), 'name': 'Testdrive'}
TEST_SENSOR = {'name': 'TestSensor', 'description': 'The testsensor is only for testing purposes.'}
TEST_UNIT = {'name': "km/h"}
TEST_VALUETYPE = {'name': int.__name__}
TEST_SIGNAL = {'name': "TestSignal"}
TEST_AGGREGATION = {'timestamp': datetime.now()}
TEST_RECORD = {'start_mileage': 0, 'end_mileage': 100, 'drive_length': 100, 'start_time': datetime.now(),
               'end_time': datetime.now() + timedelta(minutes=60), 'filepath': "/opt/test/test_record.json"
               }
TEST_CAMPAIGN = dict(name="TestCampaign", start=datetime.now(), end=datetime.now() + timedelta(hours=5),
                     description='I am a test campaign')
TEST_DRIVER = {'name': "Testdriver", 'sex': "male", 'weight': 110, 'height': 180}


class TestDriver(EngineTestCase):

    def test_create(self):
        """Test if we can add add a new driver"""

        entity = Driver(**TEST_DRIVER)

        self.session.add(entity)
        self.session.commit()

        retval = self.session.query(Driver).filter_by(name=entity.name).first()

        self.assertIsNotNone(retval)


class TestSensor(EngineTestCase):

    def test_create_sensor(self):
        """Test if we can add the test sensor."""

        entity = Sensor(**TEST_SENSOR)
        self.session.add(entity)

        self.session.commit()

        retval = self.session.query(Sensor).filter_by(name=entity.name).first()

        self.assertIsNotNone(retval)


class TestUnit(EngineTestCase):

    def test_create_unit(self):
        """Test if we can add a unit to our database"""

        unit = Unit(**TEST_UNIT)
        self.session.add(unit)
        self.session.commit()

        retval = self.session.query(Unit).filter_by(name=unit.name).first()

        self.assertIsNotNone(retval)


class TestValuetype(EngineTestCase):

    def test_create_unit(self):
        """Test if we can add the a signal type to our database"""

        valuetype = Valuetype(**TEST_VALUETYPE)
        self.session.add(valuetype)
        self.session.commit()

        retval = self.session.query(Valuetype).filter_by(name=valuetype.name).first()

        self.assertIsNotNone(retval)


class TestVehicle(EngineTestCase):

    def test_create_vehicle(self):
        """Test if we can add a vehicle to our database"""

        entity = Vehicle(**TEST_VEHICLE)
        self.session.add(entity)
        self.session.commit()

        retval = self.session.query(Vehicle).filter_by(serial_number=entity.serial_number).first()

        self.assertIsNotNone(retval)
        self.assertIsNotNone(retval.idvehicle)


class TestCampaign(EngineTestCase):

    def test_create_drive(self):
        """Test if we can add a campaignto our database
        """

        # add the test vehicle
        campaign = Campaign(**TEST_CAMPAIGN)

        self.session.add(campaign)
        self.session.commit()

        retval = self.session.query(Campaign).filter_by(description=campaign.description).first()

        self.assertEqual(TEST_CAMPAIGN['description'], retval.description), 'The descriptions do not equal'

        self.assertIsNotNone(retval)


class TestDrive(EngineTestCase):

    def test_create_drive(self):
        """Test if we can add the a drive which depends on a vehicle to our database
        """

        drive = Drive(**TEST_DRIVE)
        drive.vehicle = Vehicle(**TEST_VEHICLE)
        drive.driver = Driver(**TEST_DRIVER)
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        self.session.add(drive)
        self.session.commit()

        retval = self.session.query(Drive).filter_by(name=drive.name).first()

        self.assertEqual(TEST_DRIVE['start'], retval.start), 'The datetimes do not equal'
        self.assertIsNotNone(retval)


class TestRecord(EngineTestCase):

    def test_add_entity(self):
        """Test if we can add a new record including dependencies to the database."""

        drive = Drive(**TEST_DRIVE)
        drive.vehicle = Vehicle(**TEST_VEHICLE)
        drive.driver = Driver(**TEST_DRIVER)
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        record = Record(**TEST_RECORD)
        record.drive = drive
        record.vehicle = drive.vehicle
        record.driver = drive.driver

        self.session.add(record)
        self.session.commit()

        retval = self.session.query(Record).filter_by(filepath=record.filepath).first()

        self.assertIsNotNone(retval)


class TestSignalEntryAdd(EngineTestCase):

    def test_add_new_signal_entry(self):
        """
        Test if we can add a new signal to the signal table
        """

        # each signal has a unit, valuetype and a sensor it belongs to
        signal = Signal(**TEST_SIGNAL)
        signal.valuetype = Valuetype(**TEST_VALUETYPE)
        signal.sensor = Sensor(**TEST_SENSOR)
        signal.unit = Unit(**TEST_UNIT)

        self.session.add(signal)
        self.session.commit()

        result = self.session.query(Signal).filter_by(name=signal.name).first()

        self.assertIsNotNone(result)


class TestAggregatedSignalTableCreation(EngineTestCase):

    def setUp(self):
        super().setUp()

        # populate the database with the required test data
        signal = Signal(**TEST_SIGNAL)
        signal.valuetype = Valuetype(**TEST_VALUETYPE)
        signal.sensor = Sensor(**TEST_SENSOR)
        signal.unit = Unit(**TEST_UNIT)

        self.session.add(signal)
        self.session.commit()

        self.signal = self.session.query(Signal).filter_by(name=signal.name).first()

    def test_signal_table_creation_based_on_signal_entry(self):
        """Test if we can create a new aggregated signal table"""

        # get the value type of the signal
        valuetype = self.session.query(Valuetype).get(self.signal.idvaluetype)

        # create a new signal table based on this type
        create_signal_table(Base.metadata, Base, self.signal.name, valuetype.name, True)

        # let the engine metadata update its internal model according to the tables in the database
        Base.metadata.reflect(self.engine)

        # now check if our previously created table exists
        self.assertTrue(signal_table_name(self.signal.name, True) in Base.metadata.tables.keys())

    def test_insert_into_created_table(self):
        """Test if we can insert a new entry to a dynamically created aggregated signal table."""

        drive = Drive(**TEST_DRIVE)
        drive.vehicle = Vehicle(**TEST_VEHICLE)
        drive.driver = Driver(**TEST_DRIVER)
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        # we have to add an entry to the aggregation table
        aggregation = Aggregation(**TEST_AGGREGATION)
        aggregation.drive = drive
        self.session.add(aggregation)
        self.session.commit()

        # get the value type of the signal
        valuetype = self.session.query(Valuetype).get(self.signal.idvaluetype)

        # create a new signal table based on this type
        model, table = create_signal_table(Base.metadata, Base, self.signal.name, valuetype.name, True)

        # let the engine metadata update its internal model according to the tables in the database
        Base.metadata.reflect(self.engine)

        test_data = {
            'value': 500,
            'timestamp': datetime.now(),
            'idaggregation': aggregation.idaggregation
        }

        insert_statement = table.insert().values(**test_data)
        self.session.execute(insert_statement)
        self.session.commit()

        result = self.session.query(table).all()
        self.assertEqual(1, len(result), 'Check if only one result is returned.')

        for key in test_data:
            self.assertEqual(test_data[key], getattr(result[0], key))


class TestSignalTableCreation(EngineTestCase):

    def setUp(self):
        super().setUp()

        # populate the database with the required test data
        signal = Signal(**TEST_SIGNAL)
        signal.valuetype = Valuetype(**TEST_VALUETYPE)
        signal.sensor = Sensor(**TEST_SENSOR)
        signal.unit = Unit(**TEST_UNIT)

        self.session.add(signal)
        self.session.commit()

        self.signal = self.session.query(Signal).filter_by(name=signal.name).first()

    def test_signal_table_creation_based_on_signal_entry(self):
        """Test if we can create a new signal table"""

        # get the value type of the signal
        valuetype = self.session.query(Valuetype).get(self.signal.idvaluetype)

        # create a new signal table based on this type
        create_signal_table(Base.metadata, Base, self.signal.name, valuetype.name)

        # let the engine metadata update its internal model according to the tables in the database
        Base.metadata.reflect(self.engine)

        # now check if our previously created table exists
        self.assertTrue(signal_table_name(self.signal.name) in Base.metadata.tables.keys())

    def test_insert_into_created_table(self):
        """Test if we can insert a new entry to a dynamically created signal table."""

        # add the test vehicle
        vehicle = Vehicle(**TEST_VEHICLE)
        driver = Driver(**TEST_DRIVER)
        drive = Drive(**TEST_DRIVE)
        drive.vehicle = vehicle
        drive.driver = driver
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        record = Record(**TEST_RECORD)
        record.vehicle = vehicle
        record.driver = driver
        record.drive = drive

        self.session.add(record)
        self.session.commit()

        test_data = {
            'timestamp': datetime.now(),
            'idrecord': record.idrecord,
            'idsignal': self.signal.idsignal,
            'idvehicle': vehicle.idvehicle
        }

        # get the value type of the signal
        valuetype = self.session.query(Valuetype).get(self.signal.idvaluetype)

        # create a new signal table based on this type
        model, table = create_signal_table(Base.metadata, Base, self.signal.name, valuetype.name)

        # let the engine metadata update its internal model according to the tables in the database
        Base.metadata.reflect(self.engine)

        entity = model(timestamp=datetime.now())

        for key in test_data:
            setattr(entity, key, test_data[key])

        self.session.add(entity)
        self.session.commit()

        result = self.session.query(table).all()

        self.assertEqual(1, len(result))

        for key in test_data:
            self.assertEqual(test_data[key], getattr(result[0], key))


class TestSignalTableCreationMultiple(EngineTestCase):

    def setUp(self):
        super().setUp()

        # populate the database with the required test data
        signal = Signal(**TEST_SIGNAL)
        signal.valuetype = Valuetype(**TEST_VALUETYPE)
        signal.sensor = Sensor(**TEST_SENSOR)
        signal.unit = Unit(**TEST_UNIT)

        self.session.add(signal)
        self.session.commit()

        self.signal = self.session.query(Signal).filter_by(name=signal.name).first()

    def test_create_multiple_signal_tables(self):
        # add the test vehicle
        vehicle = Vehicle(**TEST_VEHICLE)
        driver = Driver(**TEST_DRIVER)
        drive = Drive(**TEST_DRIVE)
        drive.vehicle = vehicle
        drive.driver = driver
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        record = Record(**TEST_RECORD)
        record.vehicle = vehicle
        record.driver = driver
        record.drive = drive

        self.session.add(record)

        [create_signal_table(Base.metadata, Base, "{}".format(i), random.choice(list(_TYPE_MIXIN_MAP.keys()))) for i in
         range(100)]

        self.session.commit()
        for i in range(100):
            model, table = create_signal_table(Base.metadata, Base, "{}".format(i),
                                               random.choice(list(_TYPE_MIXIN_MAP.keys())))

            ins = table.insert().values(timestamp=datetime.now(), idrecord=record.idrecord,
                                        idsignal=self.signal.idsignal,
                                        idvehicle=vehicle.idvehicle)

            self.session.execute(ins)
