# To run this test do:
# pytest --pyargs reahlbalancesheet_dev.test_reahlbalancesheet
# or
# reahl unit
#
# To set up a demo database for playing with, do:
# pytest -o python_functions=demo_setup --pyargs reahlbalancesheet_dev.test_reahlbalancesheet
# or
# reahl demosetup


from reahl.tofu.pytestsupport import with_fixtures

from app.reahlbalancesheet import Customer

from reahl.sqlalchemysupport_dev.fixtures import SqlAlchemyFixture


@with_fixtures(SqlAlchemyFixture)
def demo_setup(sql_alchemy_fixture):
    sql_alchemy_fixture.commit = True
    Customer(email_address='friend1@some.org', name='Friend1').save()
    Customer(email_address='friend2@some.org', name='Friend2').save()
    Customer(email_address='friend3@some.org', name='Friend3').save()
    Customer(email_address='friend4@some.org', name='Friend4').save()
