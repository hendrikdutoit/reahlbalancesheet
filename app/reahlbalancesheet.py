from reahl.web.fw import UserInterface, Widget
from reahl.web.bootstrap.page import HTML5Page
from reahl.web.bootstrap.ui import Div, H, P, FieldSet
from reahl.web.bootstrap.navbar import Navbar, ResponsiveLayout
from reahl.web.bootstrap.navs import Nav
from reahl.web.bootstrap.grid import Container
from reahl.web.bootstrap.forms import TextInput, Form, FormLayout, Button
from reahl.web.bootstrap.files import FileUploadInput
from reahl.component.modelinterface import (
    exposed,
    Field,
    Action,
    Event,
    DateField,
    FileField,
)
from reahl.sqlalchemysupport import Session, Base
from reahl.web.plotly import Chart
import plotly.graph_objects as pg
from sqlalchemy import Column, Integer, UnicodeText, Date, LargeBinary


class CustomerPage(HTML5Page):
    def __init__(self, view, bookmarks):
        super().__init__(view)
        self.body.use_layout(Container())

        layout = ResponsiveLayout('md', colour_theme='dark', bg_scheme='primary')
        navbar = Navbar(view, css_id='my_nav').use_layout(layout)
        navbar.layout.set_brand_text('Customers')
        # navbar.layout.add(TextNode(view, 'All your customers'))
        navbar.layout.add(Nav(view).with_bookmarks(bookmarks))

        self.body.add_child(navbar)
        # self.body.add_child(CustomerBookPanel(view))


class HomePage(CustomerPage):
    def __init__(self, view, main_bookmarks):
        super().__init__(view, main_bookmarks)
        self.body.add_child(CustomerPanel(view))


class AddCustomerPage(CustomerPage):
    def __init__(self, view, main_bookmarks):
        super().__init__(view, main_bookmarks)
        self.body.add_child(CustomerForm(view))


class CustomerForm(Form):
    def __init__(self, view):
        super().__init__(view, 'customer_form')

        inputs = self.add_child(FieldSet(view, legend_text='Add a customer'))
        inputs.use_layout(FormLayout())

        new_customer = Customer()
        inputs.layout.add_input(TextInput(self, new_customer.fields.surname))
        inputs.layout.add_input(TextInput(self, new_customer.fields.name))
        inputs.layout.add_input(TextInput(self, new_customer.fields.dob))

        # attachments = self.add_child(FieldSet(view, legend_text='Attach files'))
        # attachments.use_layout(FormLayout())
        inputs.layout.add_input(
            FileUploadInput(self, new_customer.fields.uploaded_files), hide_label=True
        )

        inputs.add_child(Button(self, new_customer.events.save))


class CustomerPanel(Div):
    def __init__(self, view):
        super().__init__(view)

        self.add_child(H(view, 1, text='Customers'))

        # self.add_child(CustomerForm(view))

        for customer in Session.query(Customer).all():
            self.add_child(CustomerBox(view, customer))


class CustomerBox(Widget):
    def __init__(self, view, customer):
        super().__init__(view)
        self.add_child(
            P(view, text='%s %s, %s' % (customer.dob, customer.surname, customer.name))
        )


class CustomerUI(UserInterface):
    def assemble(self):
        home = self.define_view('/', title='Show')
        add = self.define_view('/add', title='Add')
        graph = self.define_view('/graph', title='Graph')

        # self.define_transition(Customer.events.save, home, home)
        bookmarks = [v.as_bookmark(self) for v in [home, add, graph]]
        home.set_page(HomePage.factory(bookmarks))
        add.set_page(AddCustomerPage.factory(bookmarks))
        graph.set_page(GraphPage.factory(bookmarks))

        self.define_transition(Customer.events.save, add, graph)
        self.define_transition(GraphPage.events.back, graph, home)


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    surname = Column(UnicodeText)
    name = Column(UnicodeText)
    dob = Column(Date)
    bsfilename = Column(UnicodeText)
    bscontents = Column(LargeBinary)

    @exposed
    def fields(self, fields):
        fields.surname = Field(label='Surname', required=True)
        fields.name = Field(label='Name', required=True)
        fields.dob = DateField(label='Date of Birth', required=True)
        fields.uploaded_files = FileField(
            allow_multiple=False, max_size_bytes=4 * 1000 * 1000, max_files=1
        )

    def save(self):
        self.bsfilename = self.uploaded_files.filename
        self.bscontents = self.uploaded_files.contents
        Session.add(self)

    @exposed('save')
    def events(self, events):
        events.save = Event(label='Save', action=Action(self.save))


class GraphPage(CustomerPage):
    def __init__(self, view, main_bookmarks):
        super().__init__(view, main_bookmarks)

        fig1 = self.create_bar_chart_figure()
        self.body.add_child(Chart(view, fig1, 'bar'))

        self.add_child(Button(self, self.events.back))

    def create_line_chart_figure(self):
        x = [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec',
        ]
        fig = pg.Figure()
        fig.add_trace(
            pg.Scatter(
                x=x, y=[1000, 1500, 1360, 1450, 1470, 1500, 1700], name='first line'
            )
        )
        fig.add_trace(
            pg.Scatter(
                x=x,
                y=[
                    100,
                    200,
                    300,
                    450,
                    530,
                    570,
                    600,
                    640,
                    630,
                    690,
                ],
                name='second line',
            )
        )
        fig.update_layout(
            title="Line chart",
            hovermode="x unified",
            xaxis_title="X Axis Title",
            yaxis_title="Y Axis Title",
        )
        return fig

    def create_bar_chart_figure(self):
        fig = pg.Figure()
        fig.add_trace(pg.Bar(y=[2, 3, 1], x=['foo', 'bar', 'baz']))
        fig.update_layout(
            title="Bar chart", xaxis_title="X Axis Title", yaxis_title="Y Axis Title"
        )
        return fig

    def back(self):
        pass

    @exposed('back')
    def events(self, events):
        events.back = Event(label='Back', action=Action(self.back))
