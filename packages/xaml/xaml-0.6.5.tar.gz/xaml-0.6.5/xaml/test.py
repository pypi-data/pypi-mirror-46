'''
Tests for Xaml
'''
from __future__ import unicode_literals
from unittest import TestCase, main
from textwrap import dedent
import xaml
from xaml import Xaml, PPLCStream, Token, Tokenizer, TokenType, State, ML, XamlError, ParseError

s = State
tt = TokenType


class TestML(TestCase):

    def test_xml(self):
        for values in (
                {'type':'xml'},
                {'type':'xml', 'version':'1.0'},
                {'type':'xml', 'version':'1.0', 'encoding':'utf-8'},
                ):
            meta = ML(values)
            self.assertEqual(str(meta), '<?xml version="1.0"?>\n')
            self.assertEqual(meta.bytes(), '<?xml version="1.0" encoding="utf-8"?>\n'.encode('utf-8'))

    def test_html5(self):
        for values in (
                {'type':'html'},
                {'type':'html', 'version':'5'},
                ):
            meta = ML(values)
            self.assertEqual(str(meta), '<!DOCTYPE html>\n')
            self.assertEqual(meta.bytes(), '<!DOCTYPE html>\n'.encode('utf-8'))

    def test_html4_strict(self):
        for values in (
                {'type':'html', 'version':'4'},
                {'type':'html', 'version':'4-strict'},
                ):
            meta = ML(values)
            self.assertEqual(str(meta), '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n')
            self.assertEqual(meta.bytes(), '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'.encode('utf-8'))

    def test_html4_transitional(self):
        for values in (
                {'type':'html', 'version':'4-transitional'},
                ):
            meta = ML(values)
            self.assertEqual(str(meta), '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n')
            self.assertEqual(meta.bytes(), '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n'.encode('utf-8'))

class TestXaml(TestCase):

    maxDiff = None

    def test_empty_doc(self):
        Xaml('').document.pages[0].bytes()

    def test_mostly_empty_doc(self):
        self.assertEqual(
                Xaml('!!! html\n!!! vim: fileencoding=utf-8'.encode('utf-8')).document.pages[0].string(),
                '<!DOCTYPE html>\n',
                )

    def test_bad_meta_type(self):
        input = ('''!!! xaml1.0''')
        self.assertRaises(ParseError, Xaml, input)

    def test_content_xmling(self):
        result = Xaml('<howdy!>').document.pages[0].string()
        expected = '&lt;howdy!&gt;'
        self.assertEqual(expected, result)

    def test_initial_blank_line(self):
        input = (
            '''\n'''
            '''~opentag\n'''
            '''    ~data\n'''
            '''        :python\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            '''\n'''
            '''    ~data\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''        <script type="text/python">\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            '''        </script>\n'''
            '''    </data>\n'''
            '''    <data/>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_initial_blank_line_and_meta(self):
        input = (
            '''\n'''
            '''!!! xml1.0\n'''
            '''~opentag\n'''
            '''    ~data\n'''
            '''        :python\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            '''\n'''
            '''    ~data\n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<opentag>\n'''
            '''    <data>\n'''
            '''        <script type="text/python">\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            '''        </script>\n'''
            '''    </data>\n'''
            '''    <data/>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_python_filter(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''        :python\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            '''\n'''
            '''    ~data\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''        <script type="text/python">\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            '''        </script>\n'''
            '''    </data>\n'''
            '''    <data/>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_python_filter_as_last(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''        :python\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''        <script type="text/python">\n'''
            '''            1 & 2\n'''
            '''            5 < 9\n'''
            '''        </script>\n'''
            '''    </data>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_meta_coding(self):
        result = Xaml('!!! coding: cp1252\n!!! xml'.encode('cp1252')).document.pages[0].bytes()
        expected = '<?xml version="1.0" encoding="utf-8"?>\n'.encode('utf-8')
        self.assertEqual(expected, result)

    # def test_double_documents(self):
    #     input = (
    #         '''!!!xml1.0\n'''
    #         '''~AccessRequest xml:lang='en-US'\n'''
    #         '''    ~AccessLicenseNumber: YourLicenseNumber\n'''
    #         '''    ~UserId: YourUserID\n'''
    #         '''    ~Password: YourPassword\n'''
    #         '''!!!xml1.0\n'''
    #         '''~TrackRequest xml:lang='en-US'\n'''
    #         '''    ~Request\n'''
    #         '''        ~TransactionReference\n'''
    #         '''            ~CustomerContext: Your Test Case Summary Description\n'''
    #         '''            ~XpciVersion: 1.0\n'''
    #         '''        ~RequestAction: Track\n'''
    #         '''        ~RequestOption: activity\n'''
    #         '''    ~TrackingNumber: YourTrackingNumber\n'''
    #         )
    #     expected = (
    #         '''<?xml version="1.0"?>\n'''
    #         '''<AccessRequest xml:lang="en-US">\n'''
    #         '''    <AccessLicenseNumber>YourLicenseNumber</AccessLicenseNumber>\n'''
    #         '''    <UserId>YourUserID</UserId>\n'''
    #         '''    <Password>YourPassword</Password>\n'''
    #         '''</AccessRequest>\n'''
    #         '''<?xml version="1.0"?>\n'''
    #         '''<TrackRequest xml:lang="en-US">\n'''
    #         '''    <Request>\n'''
    #         '''        <TransactionReference>\n'''
    #         '''            <CustomerContext>Your Test Case Summary Description</CustomerContext>\n'''
    #         '''            <XpciVersion>1.0</XpciVersion>\n'''
    #         '''        </TransactionReference>\n'''
    #         '''        <RequestAction>Track</RequestAction>\n'''
    #         '''        <RequestOption>activity</RequestOption>\n'''
    #         '''    </Request>\n'''
    #         '''    <TrackingNumber>YourTrackingNumber</TrackingNumber>\n'''
    #         '''</TrackRequest>'''
    #         ).encode('utf-8')
    #     self.assertSequenceEqual(expected.split('\n'), Xaml(input).document.pages[0].string().split('\n'))

    def test_xmlify_str_attr(self):
        result = Xaml("~Test colors='blue:days_left<=days_warn and days_left>0;red:days_left<=0;'").document.pages[0].string()
        expected = '<Test colors="blue:days_left&lt;=days_warn and days_left&gt;0;red:days_left&lt;=0;"/>'
        self.assertEqual(expected, result)

    def test_comment(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        // a random comment\n'''
            '''        // a scheduled comment\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <!--\n'''
            '''         |  a random comment\n'''
            '''         |  a scheduled comment\n'''
            '''        -->\n'''
            '''\n'''
            '''    </data>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_nested_comments(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        // testing\n'''
            '''\n'''
            '''        ~record view='ir.ui.view' #testing\n'''
            '''            @name: Testing\n'''
            '''            @model: some.table\n'''
            '''            @arch type='xml'\n'''
            '''                ~form\n'''
            '''                    ~group\n'''
            '''                        @name\n'''
            '''                        @description\n'''
            '''                    ~group\n'''
            '''                        @price\n'''
            '''                        @year\n'''
            '''\n'''
            '''        ~record view='ir.actions.act_window' #more_testing\n'''
            '''            @name: More Testing\n'''
            '''            @res_madel: some.table\n'''
            '''            @view_type: form\n'''
            '''            @view_mode: form,tree\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <!--\n'''
            '''         |  testing\n'''
            '''        -->\n'''
            '''\n'''
            '''        <record id="testing" view="ir.ui.view">\n'''
            '''            <field name="name">Testing</field>\n'''
            '''            <field name="model">some.table</field>\n'''
            '''            <field name="arch" type="xml">\n'''
            '''                <form>\n'''
            '''                    <group>\n'''
            '''                        <field name="name"/>\n'''
            '''                        <field name="description"/>\n'''
            '''                    </group>\n'''
            '''                    <group>\n'''
            '''                        <field name="price"/>\n'''
            '''                        <field name="year"/>\n'''
            '''                    </group>\n'''
            '''                </form>\n'''
            '''            </field>\n'''
            '''        </record>\n'''
            '''\n'''
            '''        <record id="more_testing" view="ir.actions.act_window">\n'''
            '''            <field name="name">More Testing</field>\n'''
            '''            <field name="res_madel">some.table</field>\n'''
            '''            <field name="view_type">form</field>\n'''
            '''            <field name="view_mode">form,tree</field>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''</opentag>'''
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_nesting_blanks(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        ~record view='ir.ui.view' #testing\n'''
            '''            @name blah='Testing'\n'''
            '''                ~form\n'''
            '''                    ~group\n'''
            '''\n'''
            '''    ~data noupdate='1'\n'''
            '''         ~record view='ir.ui.view'\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <record id="testing" view="ir.ui.view">\n'''
            '''            <field name="name" blah="Testing">\n'''
            '''                <form>\n'''
            '''                    <group/>\n'''
            '''                </form>\n'''
            '''            </field>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''\n'''
            '''    <data noupdate="1">\n'''
            '''        <record view="ir.ui.view"/>\n'''
            '''    </data>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_same_level_comments(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        ~record view='ir.ui.view' #testing\n'''
            '''\n'''
            '''        // testing\n'''
            '''\n'''
            '''        ~record view='ir.actions.act_window' #more_testing\n'''
            '''            @name: More Testing\n'''
            '''            @res_madel: some.table\n'''
            '''            @view_type: form\n'''
            '''            @view_mode: form,tree\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <record id="testing" view="ir.ui.view"/>\n'''
            '''\n'''
            '''        <!--\n'''
            '''         |  testing\n'''
            '''        -->\n'''
            '''\n'''
            '''        <record id="more_testing" view="ir.actions.act_window">\n'''
            '''            <field name="name">More Testing</field>\n'''
            '''            <field name="res_madel">some.table</field>\n'''
            '''            <field name="view_type">form</field>\n'''
            '''            <field name="view_mode">form,tree</field>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_indented_content(self):
        input = (
            '''@script\n'''
            '''    lines = text.strip().split('\\n')\n'''
            '''    while lines:\n'''
            '''        segment, lines = lines[:12], lines[12:]\n'''
            '''        _, hash, ip, _ = segment[0].split()\n'''
            '''        ascii_art = '\\n'.join(segment[1:])\n'''
            '''        result[ip] = '%s\\n\\n%s' % (hash, ascii_art)\n'''
            )
        expected = (
            '''<field name="script">\n'''
            '''    lines = text.strip().split('\\n')\n'''
            '''    while lines:\n'''
            '''        segment, lines = lines[:12], lines[12:]\n'''
            '''        _, hash, ip, _ = segment[0].split()\n'''
            '''        ascii_art = '\\n'.join(segment[1:])\n'''
            '''        result[ip] = '%s\\n\\n%s' % (hash, ascii_art)\n'''
            '''</field>'''
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_after_indented_content(self):
        input = (
            '''@script\n'''
            '''    lines = text.strip().split('\\n')\n'''
            '''    while lines:\n'''
            '''        segment, lines = lines[:12], lines[12:]\n'''
            '''        _, hash, ip, _ = segment[0].split()\n'''
            '''        ascii_art = '\\n'.join(segment[1:])\n'''
            '''        result[ip] = '%s\\n\\n%s' % (hash, ascii_art)\n'''
            '''\n'''
            '''@something_else\n'''
            )
        expected = (
            '''<field name="script">\n'''
            '''    lines = text.strip().split('\\n')\n'''
            '''    while lines:\n'''
            '''        segment, lines = lines[:12], lines[12:]\n'''
            '''        _, hash, ip, _ = segment[0].split()\n'''
            '''        ascii_art = '\\n'.join(segment[1:])\n'''
            '''        result[ip] = '%s\\n\\n%s' % (hash, ascii_art)\n'''
            '''</field>\n'''
            '''\n'''
            '''<field name="something_else"/>'''
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_backslashes_not_removed(self):
        input = (
            '''!!!html\n'''
            '''~html\n'''
            '''    ~body\n'''
            '''        ~div .container\n'''
            '''            ~h1: Cam's Pizzeria\n'''
            '''            ~div .row\n'''
            '''                ~form action="#" onsubmit="alert('Thanks for clicking! This button doesn\\'t do anything because this is a fake pizzeria :\)')"\n'''
            '''                    ~input type="submit" value="Contact Us"\n'''
            )
        expected = (
            """<!DOCTYPE html>\n"""
            """<html>\n"""
            """    <head>\n"""
            """        <meta charset="utf-8">\n"""
            """    </head>\n"""
            """    <body>\n"""
            """        <div class="container">\n"""
            """            <h1>Cam's Pizzeria</h1>\n"""
            """            <div class="row">\n"""
            """                <form action="#" onsubmit="alert('Thanks for clicking! This button doesn\\'t do anything because this is a fake pizzeria :\\)')">\n"""
            """                    <input type="submit" value="Contact Us">\n"""
            """                </form>\n"""
            """            </div>\n"""
            """        </div>\n"""
            """    </body>\n"""
            """</html>"""
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_slash_only_preserves_white_space(self):
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    ~items: /\n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<sample>\n'''
            '''    <items> </items>\n'''
            '''</sample>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    ~items:   /\n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<sample>\n'''
            '''    <items>   </items>\n'''
            '''</sample>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    ~items:    / \n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<sample>\n'''
            '''    <items>    </items>\n'''
            '''</sample>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_pipe_continuation_lines(self):
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    ~items\n'''
            '''    | options="{'this': 'that'}"\n'''
            '''    | readonly='1'\n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<sample>\n'''
            '''    <items options="{'this': 'that'}" readonly="1"/>\n'''
            '''</sample>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    ~items\n'''
            '''    | options="{'this': 'that'}"\n'''
            '''    | readonly='1'\n'''
            '''\n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<sample>\n'''
            '''    <items options="{'this': 'that'}" readonly="1"/>\n'''
            '''</sample>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    ~items\n'''
            '''    | options="{'this': 'that'}"\n'''
            '''    | readonly='1'\n'''
            '''    ~another_item: Hello!\n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<sample>\n'''
            '''    <items options="{'this': 'that'}" readonly="1"/>\n'''
            '''    <another_item>Hello!</another_item>\n'''
            '''</sample>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    @some_field\n'''
            '''    | options="{'this': 'that'}"\n'''
            '''    | readonly='1'\n'''
            '''    @another_field\n'''
            )
        expected = (
            '''<?xml version="1.0"?>\n'''
            '''<sample>\n'''
            '''    <field name="some_field" options="{'this': 'that'}" readonly="1"/>\n'''
            '''    <field name="another_field"/>\n'''
            '''</sample>'''
            )
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].string())
        input = (
            '''~openerp\n'''
            '''    ~data noupdate='0'\n'''
            '''\n'''
            '''        ~record model='ir.ui.view' #sample_request_form\n'''
            '''            @name: sample.request.form\n'''
            '''            @model: sample.request\n'''
            '''            @arch type='xml'\n'''
            '''                ~form $Sample_Request version='7.0' edit="[('is_historical','=',False),('state','!=','complete')]" setup='onload(user_id, contact_id, partner_id, ship_to_id, request_type, lead_id, lead_partner, lead_contact, context)'\n'''
            '''                    ~header\n'''
            '''                        ~button @button_sample_submit $Submit .oe_edit_hide type='object' attrs="{'invisible': ['|',('state','!=', 'draft'),('product_ids','=',[])]}"\n'''
            '''                        ~button @button_sample_complete $Done .oe_edit_hide type='object' attrs="{'invisible': [('state','!=','production')]}"\n'''
            '''                        ~button @button_sample_reprint $Reprint_Labels .oe_edit_hide type='object' attrs="{'invisible': [('state','!=','complete')]}"\n'''
            '''                        @state widget='statusbar'\n'''
            '''                    @id invisible='1'\n'''
            '''                    @ref_num invisible='1'\n'''
            '''                    @partner_is_company invisible='1'\n'''
            '''                    @is_historical invisible='1'\n'''
            '''                    ~div .oe_title\n'''
            '''                        ~h1\n'''
            '''                            @ref_name attrs="{'invisible': [('id','=',False)]}"\n'''
            '''                    ~group col='5'\n'''
            '''                        ~group colspan='2'\n'''
            '''                            @user_id readonly="1" options="{'limit':15, 'create':0, 'create_edit':0}"\n'''
            '''                            @request_type\n'''
            '''                            | on_change='onchange_request_type(user_id, contact_id, partner_id, ship_to_id, request_type, lead_id, lead_partner, lead_contact, context)'\n'''
            '''                            | widget='radio'\n'''
            '''                            | writeonly="groups('base.group_sale_salesman,sample.group_sample_user')"\n'''
            )
        expected = (
            '''<openerp>\n'''
            '''    <data noupdate="0">\n'''
            '''\n'''
            '''        <record id="sample_request_form" model="ir.ui.view">\n'''
            '''            <field name="name">sample.request.form</field>\n'''
            '''            <field name="model">sample.request</field>\n'''
            '''            <field name="arch" type="xml">\n'''
            '''                <form edit="[('is_historical','=',False),('state','!=','complete')]" setup="onload(user_id, contact_id, partner_id, ship_to_id, request_type, lead_id, lead_partner, lead_contact, context)" string="Sample Request" version="7.0">\n'''
            '''                    <header>\n'''
            '''                        <button name="button_sample_submit" class="oe_edit_hide" attrs="{'invisible': ['|',('state','!=', 'draft'),('product_ids','=',[])]}" string="Submit" type="object"/>\n'''
            '''                        <button name="button_sample_complete" class="oe_edit_hide" attrs="{'invisible': [('state','!=','production')]}" string="Done" type="object"/>\n'''
            '''                        <button name="button_sample_reprint" class="oe_edit_hide" attrs="{'invisible': [('state','!=','complete')]}" string="Reprint Labels" type="object"/>\n'''
            '''                        <field name="state" widget="statusbar"/>\n'''
            '''                    </header>\n'''
            '''                    <field name="id" invisible="1"/>\n'''
            '''                    <field name="ref_num" invisible="1"/>\n'''
            '''                    <field name="partner_is_company" invisible="1"/>\n'''
            '''                    <field name="is_historical" invisible="1"/>\n'''
            '''                    <div class="oe_title">\n'''
            '''                        <h1>\n'''
            '''                            <field name="ref_name" attrs="{'invisible': [('id','=',False)]}"/>\n'''
            '''                        </h1>\n'''
            '''                    </div>\n'''
            '''                    <group col="5">\n'''
            '''                        <group colspan="2">\n'''
            '''                            <field name="user_id" options="{'limit':15, 'create':0, 'create_edit':0}" readonly="1"/>\n'''
            '''                            <field name="request_type" on_change="onchange_request_type(user_id, contact_id, partner_id, ship_to_id, request_type, lead_id, lead_partner, lead_contact, context)" widget="radio" writeonly="groups('base.group_sale_salesman,sample.group_sample_user')"/>\n'''
            '''                        </group>\n'''
            '''                    </group>\n'''
            '''                </form>\n'''
            '''            </field>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''</openerp>'''
            )
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].string())

    def test_trailing_slashes_are_removed(self):
        input = (
            '''!!!xml1.0\n'''
            '''~sample\n'''
            '''    ~items: here's a line with blanks at the end  /\n'''
            )
        expected = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<sample>\n'''
            '''    <items>here's a line with blanks at the end  </items>\n'''
            '''</sample>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_random_content(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        ~record #this_id\n'''
            '''            ~button #but1 $Click_Me!\n'''
            '''            or\n'''
            '''            ~button #but2 $Cancel\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <record id="this_id">\n'''
            '''            <button id="but1" string="Click Me!"/>\n'''
            '''            or\n'''
            '''            <button id="but2" string="Cancel"/>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''</opentag>'''
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_random_content_with_newlines_after(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        ~record #this_id\n'''
            '''            ~button #but1 $Click_Me!\n'''
            '''            or\n'''
            '''\n'''
            '''            ~button #but2 $Cancel\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <record id="this_id">\n'''
            '''            <button id="but1" string="Click Me!"/>\n'''
            '''            or\n'''
            '''\n'''
            '''            <button id="but2" string="Cancel"/>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_random_content_with_newlines_around(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        ~record #this_id\n'''
            '''            ~button #but1 $Click_Me!\n'''
            '''\n'''
            '''            or\n'''
            '''\n'''
            '''            ~button #but2 $Cancel\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <record id="this_id">\n'''
            '''            <button id="but1" string="Click Me!"/>\n'''
            '''\n'''
            '''            or\n'''
            '''\n'''
            '''            <button id="but2" string="Cancel"/>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''</opentag>'''
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_random_content_with_newlines_before(self):
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''\n'''
            '''        ~record #this_id\n'''
            '''            ~button #but1 $Click_Me!\n'''
            '''\n'''
            '''            or\n'''
            '''            ~button #but2 $Cancel\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''\n'''
            '''        <record id="this_id">\n'''
            '''            <button id="but1" string="Click Me!"/>\n'''
            '''\n'''
            '''            or\n'''
            '''            <button id="but2" string="Cancel"/>\n'''
            '''        </record>\n'''
            '''\n'''
            '''    </data>\n'''
            '''</opentag>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_simple(self):
        input = (
            '''~opentag\n'''
            '''    ~level_one\n'''
            '''        ~field @code: Code goes here\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <level_one>\n'''
            '''        <field name="code">Code goes here</field>\n'''
            '''    </level_one>\n'''
            '''</opentag>'''
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_nested(self):
        input = (
            '''~openerp\n'''
            '''   ~record #fax_id view='ui.ir.view'\n'''
            '''      @name: Folders\n'''
            '''      @arch type='xml'\n'''
            '''         ~form $Folders version='7.0'\n'''
            '''            ~group\n'''
            '''               ~group\n'''
            '''                  @id invisibility='1'\n'''
            '''                  @name\n'''
            '''                  @path\n'''
            '''               ~group\n'''
            '''                  @folder_type\n'''
            )
        expected = (
            '''<openerp>\n'''
            '''    <record id="fax_id" view="ui.ir.view">\n'''
            '''        <field name="name">Folders</field>\n'''
            '''        <field name="arch" type="xml">\n'''
            '''            <form string="Folders" version="7.0">\n'''
            '''                <group>\n'''
            '''                    <group>\n'''
            '''                        <field name="id" invisibility="1"/>\n'''
            '''                        <field name="name"/>\n'''
            '''                        <field name="path"/>\n'''
            '''                    </group>\n'''
            '''                    <group>\n'''
            '''                        <field name="folder_type"/>\n'''
            '''                    </group>\n'''
            '''                </group>\n'''
            '''            </form>\n'''
            '''        </field>\n'''
            '''    </record>\n'''
            '''</openerp>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_meta_closing(self):
        result = Xaml('!!! xml1.0').document.pages[0].bytes()
        self.assertEqual(
                '<?xml version="1.0" encoding="utf-8"?>\n'.encode('utf-8'),
                result,
                )

    # TODO: enable this test once encodings besides utf-8 are supported
    # def test_meta_xml_non_utf_encoding(self):
    #     result = Xaml('!!! xml1.0 encoding="cp1252"').document.pages[0].string()
    #     self.assertEqual(
    #             '<?xml version="1.0" encoding="cp1252"?>\n'.encode('utf-8'),
    #             result,
    #             )

    def test_meta_xml_utf_encoding(self):
        doc = Xaml('!!! xml1.0 encoding="utf-8"').document
        self.assertEqual(
                '<?xml version="1.0" encoding="utf-8"?>\n'.encode('utf-8'),
                doc.pages[0].bytes(),
                )
        self.assertEqual(
                '<?xml version="1.0"?>\n',
                doc.pages[0].string(),
                )

    def test_element_closing(self):
        result = Xaml('~opentag').document.pages[0].bytes()
        self.assertEqual(
                '<opentag/>'.encode('utf-8'),
                result,
                )

    def test_filter(self):
        input = (
            '''-view = 'ir.ui.view'\n'''
            '''-folder_model = 'fnx.fs.folder'\n'''
            '''-files_model = 'fnx.fs.file'\n'''
            '''~openerp\n'''
            '''    ~data\n'''
            '''        ~menuitem @FnxFS #fnx_file_system groups='consumer'\n'''
            '''        ~record #fnx_fs_folders_tree model=view\n'''
            '''            @name: Folders\n'''
            '''            @model: =folder_model\n'''
            '''            @arch type='xml'\n'''
            '''                ~tree $Folders version='7.0'\n'''
            '''                    @path\n'''
            '''                    @folder_type\n'''
            '''                    @description\n'''
            )
        expected = (
            '''<openerp>\n'''
            '''    <data>\n'''
            '''        <menuitem name="FnxFS" id="fnx_file_system" groups="consumer"/>\n'''
            '''        <record id="fnx_fs_folders_tree" model="ir.ui.view">\n'''
            '''            <field name="name">Folders</field>\n'''
            '''            <field name="model">fnx.fs.folder</field>\n'''
            '''            <field name="arch" type="xml">\n'''
            '''                <tree string="Folders" version="7.0">\n'''
            '''                    <field name="path"/>\n'''
            '''                    <field name="folder_type"/>\n'''
            '''                    <field name="description"/>\n'''
            '''                </tree>\n'''
            '''            </field>\n'''
            '''        </record>\n'''
            '''    </data>\n'''
            '''</openerp>'''
            )
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_filter_2(self):
        input = (
            '''-view = 'ir.ui.view'\n'''
            '''-folder_model = 'fnx.fs.folder'\n'''
            '''-files_model = 'fnx.fs.file'\n'''
            '''-action = 'ir.actions.act_window'\n'''
            '''~openerp\n'''
            '''    ~data\n'''
            '''        ~menuitem @FnxFS #fnx_file_system groups='consumer'\n'''
            '''        ~record #fnx_fs_folders_tree model=view\n'''
            '''            @name: Folders\n'''
            '''            @model: =folder_model\n'''
            '''            @arch type='xml'\n'''
            '''                ~tree $Folders version='7.0'\n'''
            '''                    @path\n'''
            '''                    @folder_type\n'''
            '''                    @description\n'''
            '''        ~record model=action #action_fnx\n'''
            '''            @name: An Action\n'''
            '''            @res_model: = folder_model\n'''
            '''            @view_type: form\n'''
            '''            @view_id ref='something'\n'''
            '''            @view_mode: form,tree\n'''
            )
        expected = (
            '''<openerp>\n'''
            '''    <data>\n'''
            '''        <menuitem name="FnxFS" id="fnx_file_system" groups="consumer"/>\n'''
            '''        <record id="fnx_fs_folders_tree" model="ir.ui.view">\n'''
            '''            <field name="name">Folders</field>\n'''
            '''            <field name="model">fnx.fs.folder</field>\n'''
            '''            <field name="arch" type="xml">\n'''
            '''                <tree string="Folders" version="7.0">\n'''
            '''                    <field name="path"/>\n'''
            '''                    <field name="folder_type"/>\n'''
            '''                    <field name="description"/>\n'''
            '''                </tree>\n'''
            '''            </field>\n'''
            '''        </record>\n'''
            '''        <record id="action_fnx" model="ir.actions.act_window">\n'''
            '''            <field name="name">An Action</field>\n'''
            '''            <field name="res_model">fnx.fs.folder</field>\n'''
            '''            <field name="view_type">form</field>\n'''
            '''            <field name="view_id" ref="something"/>\n'''
            '''            <field name="view_mode">form,tree</field>\n'''
            '''        </record>\n'''
            '''    </data>\n'''
            '''</openerp>'''
            ).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())

    def test_dynamic(self):
        order = ['first', 'second', 'third']
        input = '\n'.join([
            '''~the_page''',
            '''    ~an_ordered_list''',
            '''        -for item in args.order:''',
            '''            ~number order=item''',
            ])
        expected = '\n'.join([
            '''<the_page>''',
            '''    <an_ordered_list>''',
            '''        <number order="first"/>''',
            '''        <number order="second"/>''',
            '''        <number order="third"/>''',
            '''    </an_ordered_list>''',
            '''</the_page>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string(order=order))

    def test_tag_in_content(self):
        input = '\n'.join([
            """~div class='oe_partner oe_show_more'""",
            """    And""",
            """    ~t t-raw='number'""",
            """    more.""",
            ])
        expected = '\n'.join([
            '''<div class="oe_partner oe_show_more">''',
            '''    And''',
            '''    <t t-raw="number"/>''',
            '''    more.''',
            '''</div>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_shortcut_in_content(self):
        input = '\n'.join([
            """~div class='oe_partner oe_show_more'""",
            """    And""",
            """    @target t-raw='number'""",
            """    more.""",
            ])
        expected = '\n'.join([
            '''<div class="oe_partner oe_show_more">''',
            '''    And''',
            '''    <field name="target" t-raw="number"/>''',
            '''    more.''',
            '''</div>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_content_and_tag(self):
        input = '\n'.join([
            """~div""",
            """    ~span : Followers of selected items and""",
            """    ~span : Followers of""",
            """        @record_name .oe_inline attrs="{'invisible':[('model', '=', False)]}" readonly='1'""",
            """        and""",
            """    @partner_ids""",
            """@subject""",
            ])
        expected = '\n'.join([
            '''<div>''',
            '''    <span>Followers of selected items and</span>''',
            '''    <span>Followers of''',
            '''        <field name="record_name" class="oe_inline" attrs="{'invisible':[('model', '=', False)]}" readonly="1"/>''',
            '''        and''',
            '''    </span>''',
            '''    <field name="partner_ids"/>''',
            '''</div>''',
            '''<field name="subject"/>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_html_canvas(self):
        input = '\n'.join([
            '''!!! html5''',
            '''~html''',
            '''    ~body''',
            '''        ~canvas''',
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''    </head>''',
            '''    <body>''',
            '''        <canvas></canvas>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_html_no_head(self):
        input = '\n'.join([
            '''!!! html5''',
            '''~html''',
            '''    ~body''',
            '''        ~div .container''',
            '''            This is a test of something.''',
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''    </head>''',
            '''    <body>''',
            '''        <div class="container">''',
            '''            This is a test of something.''',
            '''        </div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_html_empty_head(self):
        input = '\n'.join([
            '''!!! html5''',
            '''~html''',
            '''    ~head''',
            '''    ~body''',
            '''        ~div .container''',
            '''            This is a test of something.''',
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''    </head>''',
            '''    <body>''',
            '''        <div class="container">''',
            '''            This is a test of something.''',
            '''        </div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_html_head(self):
        input = '\n'.join([
            '''!!! html5''',
            '''~html''',
            '''    ~head''',
            '''        ~title: my cool app!''',
            '''    ~body''',
            '''        ~div .container''',
            '''            This is a test of something.''',
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <title>my cool app!</title>''',
            '''    </head>''',
            '''    <body>''',
            '''        <div class="container">''',
            '''            This is a test of something.''',
            '''        </div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_html_void_tags(self):
        input = '\n'.join([
            '''!!! html5''',
            '''~html''',
            '''    ~head''',
            '''        ~title: my cool app!''',
            '''    ~body''',
            '''        ~area: This is a test of something.''',
            ])
        document = Xaml(input).document
        self.assertRaises(XamlError, document.pages[0].string)
        input = '\n'.join([
            '''!!! html5''',
            '''~html''',
            '''    ~head''',
            '''        ~title: my cool app!''',
            '''    ~body''',
            '''        ~area''',
            '''            This is a test of something.''',
            ])
        document = Xaml(input).document
        self.assertRaises(XamlError, document.pages[0].string)

    def test_xml_html_void_tags(self):
        input = '\n'.join([
            '''~html''',
            '''    ~area''',
            '''        ~title: my cool app!''',
            '''    ~body''',
            '''        ~div .container''',
            '''            This is a test of something.''',
            ])
        expected = '\n'.join([
            '''<html>''',
            '''    <area>''',
            '''        <title>my cool app!</title>''',
            '''    </area>''',
            '''    <body>''',
            '''        <div class="container">''',
            '''            This is a test of something.''',
            '''        </div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_html_override_html(self):
        input = '\n'.join([
            """!!! html""",
            """~html""",
            """    ~body""",
            """        ~div""",
            """            Hello!""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''    </head>''',
            '''    <body>''',
            '''        <div>''',
            '''            Hello!''',
            '''        </div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, type='html').document.pages[0].string())

    def test_xml_override_html(self):
        input = '\n'.join([
            """!!! html""",
            """!!! vim: fileencoding=utf-8""",
            """~html""",
            """    ~body""",
            """        ~div""",
            """            Hello!""",
            ])
        expected = '\n'.join([
            '''<html>''',
            '''    <body>''',
            '''        <div>''',
            '''            Hello!''',
            '''        </div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input.encode('utf-8'), doc_type='xml').document.pages[0].string())

    def test_html_default_tag(self):
        input = '\n'.join([
            """!!! html""",
            """~html""",
            """    ~body""",
            """        .container""",
            """            Hello!""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''    </head>''',
            '''    <body>''',
            '''        <div class="container">''',
            '''            Hello!''',
            '''        </div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_html_default_tag_in_snippet(self):
        input = '\n'.join([
            """.container""",
            """    Hello!""",
            ])
        expected = '\n'.join([
            '''<div class="container">''',
            '''    Hello!''',
            '''</div>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_html_element_lock_unlocks(self):
        input = '\n'.join([
            """!!!html""",
            """~html""",
            """    ~head""",
            """        ~title: Effective JavaScript: Frogger""",
            """        ~link rel='stylesheet' href='css/style.css'""",
            """    ~body""",
            """        ~script src='js/resources.js'""",
            """        ~script src='js/app.js'""",
            """        ~script src='js/engine.js'""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <title>Effective JavaScript: Frogger</title>''',
            '''        <link href="css/style.css" rel="stylesheet">''',
            '''    </head>''',
            '''    <body>''',
            '''        <script src="js/resources.js"></script>''',
            '''        <script src="js/app.js"></script>''',
            '''        <script src="js/engine.js"></script>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_multi_class(self):
        input = '\n'.join([
            """!!! html""",
            """~div .logo .circle""",
            """    ~img src='images/my_logo.svg' alt='logo'""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<div class="logo circle">''',
            '''    <img src="images/my_logo.svg" alt="logo">''',
            '''</div>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())
        input = '\n'.join([
            """!!! html""",
            """~div .circle .logo""",
            """    ~img src='images/my_logo.svg' alt='logo'""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<div class="circle logo">''',
            '''    <img src="images/my_logo.svg" alt="logo">''',
            '''</div>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    # def test_valid_html4_strict(self):
    #     input = '\n'.join([
    #         '''!!!html4s''',
    #         '''~html''',
    #         '''    ~head''',
    #         '''        ~title: Testing HTML 4 Strict''',
    #         '''    ~body''',
    #         '''        ~div .container''',
    #         '''            This is a test of something.''',
    #         ])
    #     expected = '\n'.join([
    #         '''<html>''',
    #         '''    <area>''',
    #         '''        <title>my cool app!</title>''',
    #         '''    </area>''',
    #         '''    <body>''',
    #         '''        <div class="container">''',
    #         '''            This is a test of something.''',
    #         '''        </div>''',
    #         '''    </body>''',
    #         '''</html>''',
    #         ])
    #    self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_style_not_escaped(self):
        'no xaml processing should take place inside a <style> tag'
        input = '\n'.join([
            """~style""",
            """    #image-container {""",
            """        .display: flex;""",
            """    }""",
            """~body""",
            """    <howdy!>""",
            ])
        expected = '\n'.join([
            '''<style>''',
            '''    #image-container {''',
            '''        .display: flex;''',
            '''    }''',
            '''</style>''',
            '''<body>''',
            '''    &lt;howdy!&gt;''',
            '''</body>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())
        input = '\n'.join([
            """~style""",
            """    body > ul {""",
            """        .display: flex;""",
            """    }""",
            ])
        expected = '\n'.join([
            '''<style>''',
            '''    body > ul {''',
            '''        .display: flex;''',
            '''    }''',
            '''</style>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_css_without_blank_lines(self):
        'absence of blank lines should not affect following elements'
        input = '\n'.join([
            """!!!html""",
            """~html""",
            """    ~head""",
            """        :css""",
            """            #image-container {""",
            """                .display: flex;""",
            """            }""",
            """    ~body""",
            """        <howdy!>""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <style type="text/css">''',
            '''            #image-container {''',
            '''                .display: flex;''',
            '''            }''',
            '''        </style>''',
            '''    </head>''',
            '''    <body>''',
            '''        &lt;howdy!&gt;''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_css_with_blank_lines(self):
        'presence of blank lines should not affect following elements'
        input = '\n'.join([
            """!!!html""",
            """~html""",
            """    ~head""",
            """        :css""",
            "",
            """            #image-container {""",
            """                .display: flex;""",
            """            }""",
            """    ~body""",
            """        <howdy!>""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <style type="text/css">''',
            '''            #image-container {''',
            '''                .display: flex;''',
            '''            }''',
            '''        </style>''',
            '''    </head>''',
            '''    <body>''',
            '''        &lt;howdy!&gt;''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_javascript_without_blank_lines(self):
        'absence of blank lines should not affect following elements'
        input = '\n'.join([
            """!!!html""",
            """~html""",
            """    ~head""",
            """        :javascript""",
            """            var container = document.querySelector('.a_class');""",
            """            for (var i=0; i < 3000; i++) {""",
            """                console.log('this is ' + i + '!');""",
            """            }""",
            """    ~body""",
            """        <howdy!>""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <script type="text/javascript">''',
            '''            var container = document.querySelector('.a_class');''',
            '''            for (var i=0; i < 3000; i++) {''',
            '''                console.log('this is ' + i + '!');''',
            '''            }''',
            '''        </script>''',
            '''    </head>''',
            '''    <body>''',
            '''        &lt;howdy!&gt;''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_javascript_with_blank_lines(self):
        'presence of blank lines should not affect following elements'
        input = '\n'.join([
            """!!!html""",
            """~html""",
            """    ~head""",
            """        :javascript""",
            "",
            """            var container = document.querySelector('.a_class');""",
            """            for (var i=0; i < 3000; i++) {""",
            """                console.log('this is ' + i + '!');""",
            """            }""",
            """    ~body""",
            """        <howdy!>""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <script type="text/javascript">''',
            '''            var container = document.querySelector('.a_class');''',
            '''            for (var i=0; i < 3000; i++) {''',
            '''                console.log('this is ' + i + '!');''',
            '''            }''',
            '''        </script>''',
            '''    </head>''',
            '''    <body>''',
            '''        &lt;howdy!&gt;''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_script_not_escaped(self):
        'no xaml processing should take place inside a <script> tag'
        input = '\n'.join([
            """~script""",
            """    if ( 5 < 7 &&""",
            """         .3 > .5) {""",
            """             a = false & true;""",
            """    }""",
            ])
        expected = '\n'.join([
            '''<script>''',
            '''    if ( 5 < 7 &&''',
            '''         .3 > .5) {''',
            '''             a = false & true;''',
            '''    }''',
            '''</script>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_script_not_escaped_with_blank_lines(self):
        'no xaml processing should take place inside a <script> tag, even with blank lines present'
        input = '\n'.join([
            """~script""",
            """    if ( 5 < 7 &&""",
            "",
            """    .3 > .5) {""",
            """             a = false & true;""",
            """    }""",
            ])
        expected = '\n'.join([
            '''<script>''',
            '''    if ( 5 < 7 &&''',
            '',
            '''    .3 > .5) {''',
            '''             a = false & true;''',
            '''    }''',
            '''</script>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_script_in_content(self):
        'script content is still script'
        input = '\n'.join([
            """!!! html""",
            """~html""",
            """    ~body""",
            """        ~p""",
            """            Awesome page""",
            """            :javascript""",
            """                document.write(" with JavaScript ");""",
            """            is awesome""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''    </head>''',
            '''    <body>''',
            '''        <p>''',
            '''            Awesome page''',
            '''            <script type="text/javascript">''',
            '''                document.write(" with JavaScript ");''',
            '''            </script>''',
            '''            is awesome''',
            '''        </p>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_script_and_script(self):
        'script content is still script'
        input = '\n'.join([
            """!!! html""",
            """~html""",
            """    ~body""",
            """        ~script src='some_script.js'""",
            """        ~script src='more_script.js'""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''    </head>''',
            '''    <body>''',
            '''        <script src="some_script.js"></script>''',
            '''        <script src="more_script.js"></script>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_script_and_dedent(self):
        'script content is still script'
        input = '\n'.join([
            """!!! html""",
            """~html""",
            """    ~head""",
            """        ~script src='cool_script.js'""",
            """    ~body""",
            """        ~div #main""",
            """            ~script src='some_script.js'""",
            """        ~div #content""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <script src="cool_script.js"></script>''',
            '''    </head>''',
            '''    <body>''',
            '''        <div id="main">''',
            '''            <script src="some_script.js"></script>''',
            '''        </div>''',
            '''        <div id="content"></div>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_cdata(self):
        input = '\n'.join([
            """-types = 'ip_map.type'""",
            """-commands = 'ip_map.command'""",
            """~record #command_ssh_key model=commands""",
            """    @name: ssh_key""",
            """    @string: SSH Key""",
            """    @type: text""",
            """    @sequence: 90""",
            """    @where: local""",
            """    @command: /usr/bin/ssh-keygen -lv -f /home/openerp/.ssh/known_hosts""",
            """    @script""",
            """        :cdata""",
            """            for block in Blocks(text, 12):""",
            """                _, hash, ip, _ = block[0].split()""",
            """                ip = ip.split(',')[-1]""",
            """                ascii_art = '\\n'.join(block[1:])""",
            """                result[ip] = {cmd_name: {'value': '%s\\n\\n%s' % (hash, ascii_art)}}""",
            ])
        expected = '\n'.join([
            '''<record id="command_ssh_key" model="ip_map.command">''',
            '''    <field name="name">ssh_key</field>''',
            '''    <field name="string">SSH Key</field>''',
            '''    <field name="type">text</field>''',
            '''    <field name="sequence">90</field>''',
            '''    <field name="where">local</field>''',
            '''    <field name="command">/usr/bin/ssh-keygen -lv -f /home/openerp/.ssh/known_hosts</field>''',
            '''    <field name="script">''',
            '''        <![CDATA[''',
            '''            for block in Blocks(text, 12):''',
            '''                _, hash, ip, _ = block[0].split()''',
            '''                ip = ip.split(',')[-1]''',
            '''                ascii_art = '\\n'.join(block[1:])''',
            '''                result[ip] = {cmd_name: {'value': '%s\\n\\n%s' % (hash, ascii_art)}}''',
            '''        ]]>''',
            '''    </field>''',
            '''</record>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_cdata_python(self):
        input = '\n'.join([
            """-types = 'ip_map.type'""",
            """-commands = 'ip_map.command'""",
            """~record #command_ssh_key model=commands""",
            """    @name: ssh_key""",
            """    @string: SSH Key""",
            """    @type: text""",
            """    @sequence: 90""",
            """    @where: local""",
            """    @command: /usr/bin/ssh-keygen -lv -f /home/openerp/.ssh/known_hosts""",
            """    @script""",
            """        :cdata-python""",
            """            for block in Blocks(text, 12):""",
            """                _, hash, ip, _ = block[0].split()""",
            """                ip = ip.split(',')[-1]""",
            """                ascii_art = '\\n'.join(block[1:])""",
            """                result[ip] = {cmd_name: {'value': '%s\\n\\n%s' % (hash, ascii_art)}}""",
            ])
        expected = '\n'.join([
            '''<record id="command_ssh_key" model="ip_map.command">''',
            '''    <field name="name">ssh_key</field>''',
            '''    <field name="string">SSH Key</field>''',
            '''    <field name="type">text</field>''',
            '''    <field name="sequence">90</field>''',
            '''    <field name="where">local</field>''',
            '''    <field name="command">/usr/bin/ssh-keygen -lv -f /home/openerp/.ssh/known_hosts</field>''',
            '''    <field name="script">''',
            '''        <![CDATA[''',
            '''            for block in Blocks(text, 12):''',
            '''                _, hash, ip, _ = block[0].split()''',
            '''                ip = ip.split(',')[-1]''',
            '''                ascii_art = '\\n'.join(block[1:])''',
            '''                result[ip] = {cmd_name: {'value': '%s\\n\\n%s' % (hash, ascii_art)}}''',
            '''        ]]>''',
            '''    </field>''',
            '''</record>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input).document.pages[0].string())

    def test_all_filters(self):
        input = '\n'.join([
            """!!! html""",
            """~html""",
            """    ~head""",
            """        ~title: Test Filters Page""",
            """        ~script src='somefile.js' type='text/javascript'""",
            """        ~link rel='stylesheet' href='anotherfile.css' type='text/css'""",
            """        ~link href='that_file.css' type='text/css' rel='stylesheet'""",
            """        :javascript""",
            """            if (a < b) {""",
            """                console.log('&');""",
            """            }""",
            """        :css""",
            """            body {""",
            """                background: #000;""",
            """                text-align: center;""",
            """            }""",
            """    ~body""",
            """        ~p""",
            """            Awesome page""",
            """            :javascript""",
            """                document.write(" with JavaScript ");""",
            """            ~script src='this_file.js'""",
            """            is awesome""",
            ])
        expected = '\n'.join([
            '''<!DOCTYPE html>''',
            '''<html>''',
            '''    <head>''',
            '''        <meta charset="utf-8">''',
            '''        <title>Test Filters Page</title>''',
            '''        <script src="somefile.js" type="text/javascript"></script>''',
            '''        <link href="anotherfile.css" rel="stylesheet" type="text/css">''',
            '''        <link href="that_file.css" rel="stylesheet" type="text/css">''',
            '''        <script type="text/javascript">''',
            '''            if (a < b) {''',
            '''                console.log('&');''',
            '''            }''',
            '''        </script>''',
            '''        <style type="text/css">''',
            '''            body {''',
            '''                background: #000;''',
            '''                text-align: center;''',
            '''            }''',
            '''        </style>''',
            '''    </head>''',
            '''    <body>''',
            '''        <p>''',
            '''            Awesome page''',
            '''            <script type="text/javascript">''',
            '''                document.write(" with JavaScript ");''',
            '''            </script>''',
            '''            <script src="this_file.js"></script>''',
            '''            is awesome''',
            '''        </p>''',
            '''    </body>''',
            '''</html>''',
            ])
        self.assertMultiLineEqual(expected, Xaml(input, doc_type='html').document.pages[0].string())

    def test_inline_elements(self):
        input = '\n'.join([
            '''~opentag''',
            '''    ~data''',
            '''        ~table''',
            '''            ~tr''',
            '''                ~td : ~field @some_field''',
            '''                ~td : ~field @some_other_field''',
            ])
        expected = '\n'.join([
            '''<opentag>''',
            '''    <data>''',
            '''        <table>''',
            '''            <tr>''',
            '''                <td>''',
            '''                    <field name="some_field"/>''',
            '''                </td>''',
            '''                <td>''',
            '''                    <field name="some_other_field"/>''',
            '''                </td>''',
            '''            </tr>''',
            '''        </table>''',
            '''    </data>''',
            '''</opentag>''',
            ]).encode('utf-8')
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].bytes())
        input = (
            '''~opentag\n'''
            '''    ~data\n'''
            '''        ~blockTable colWidths='78, 142' style='lines'\n'''
            '''            ~tr\n'''
            '''                ~td : ~xsl:text: Department\n'''
            '''                ~td : ~xsl:value-of select='dept'\n'''
            '''            ~tr\n'''
            '''                ~td : ~xsl:text: Request by\n'''
            '''                ~td : ~xsl:value-of select='request-by'\n'''
            )
        expected = (
            '''<opentag>\n'''
            '''    <data>\n'''
            '''        <blockTable colWidths="78, 142" style="lines">\n'''
            '''            <tr>\n'''
            '''                <td>\n'''
            '''                    <xsl:text>Department</xsl:text>\n'''
            '''                </td>\n'''
            '''                <td>\n'''
            '''                    <xsl:value-of select="dept"/>\n'''
            '''                </td>\n'''
            '''            </tr>\n'''
            '''            <tr>\n'''
            '''                <td>\n'''
            '''                    <xsl:text>Request by</xsl:text>\n'''
            '''                </td>\n'''
            '''                <td>\n'''
            '''                    <xsl:value-of select="request-by"/>\n'''
            '''                </td>\n'''
            '''            </tr>\n'''
            '''        </blockTable>\n'''
            '''    </data>\n'''
            '''</opentag>'''
            )
        self.assertSequenceEqual(expected, Xaml(input).document.pages[0].string())

class TestPPLCStream(TestCase):

    def test_get_char(self):
        sample = u'line one\nline two'
        stream = PPLCStream(sample.split('\n'))
        result = []
        while True:
            ch = stream.get_char()
            if ch is None:
                break
            result.append(ch)
        self.assertEqual(''.join(result), sample+'\n')

    def test_get_line(self):
        sample = u'line one\nline two'
        stream = PPLCStream(sample.split('\n'))
        result = []
        while True:
            line = stream.get_line()
            if line is None:
                break
            result.append(line)
        self.assertEqual(''.join(result), sample+'\n')

    def test_push_char(self):
        sample = u'line one\nline two'
        stream = PPLCStream(sample.split('\n'))
        result = []
        stream.push_char('2')
        stream.push_char('4')
        while True:
            line = stream.get_line()
            if line is None:
                break
            result.append(line)
        self.assertEqual(''.join(result), '42'+sample+'\n')

    def test_push_line(self):
        sample = u'line one\nline two'
        stream = PPLCStream(sample.split('\n'))
        result = []
        stream.push_line('line zero')
        while True:
            ch = stream.get_char()
            if ch is None:
                break
            result.append(ch)
        self.assertEqual(''.join(result), 'line zero\n'+sample+'\n')


class TestDecoding(TestCase):

    def test_error(self):
        self.assertRaises(XamlError, xaml.decode, b'!!! coding: blah')
        self.assertRaises(XamlError, xaml.decode, b'!!! coding:')
        self.assertRaises(XamlError, xaml.decode, b'!!! coding:   ')
        self.assertRaises(XamlError, xaml.decode, b'!!! coding =   ')
        self.assertRaises(XamlError, xaml.decode, b'!!! coding = nope  ')


class TestTokenizer(TestCase):

    maxDiff = None

    def test_bad_data_on_tag(self):
        self.assertRaises(ParseError, Xaml, '~record:')

    def test_bad_data_on_attribute(self):
        self.assertRaises(ParseError, Xaml, '@record:')

    def test_bad_tag(self):
        self.assertRaises(ParseError, Xaml, '~7hmm')

    def test_parens(self):
        result = list(Tokenizer([
            '''~opentag (\n''',
            '''name='value'\n''',
            ''')''',
            ]))
        self.assertEqual(
            [
                Token(tt.ELEMENT, 'opentag'),
                Token(tt.STR_ATTR, ('name', 'value'), True),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_comment(self):
        result = list(Tokenizer([
            '''// a random comment''',
            ]))
        self.assertEqual(
            [
                Token(tt.COMMENT, 'a random comment'),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_1(self):
        result = list(Tokenizer([
            '''       ''',
            ]))
        self.assertEqual(result, [Token(tt.BLANK_LINE), Token(tt.DEDENT)])

    def test_tokens_2(self):
        result = list(Tokenizer([
        '''   !!! xml''',
        ]))
        self.assertEqual(
            [
                Token(tt.INDENT),
                Token(tt.META, ('xml', '1.0')),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
            ],
            result,
            )
        self.assertEqual(None, result[0].payload)

    def test_tokens_2_1(self):
        result = list(Tokenizer([
        '''~testnames blah:="nancy"''',
        ]))
        self.assertEqual(
            [
                Token(tt.ELEMENT, 'testnames'),
                Token(tt.STR_ATTR, payload=('blah:', 'nancy'), make_safe=True),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_2_2(self):
        result = list(Tokenizer([
        '''~testnames blah\: whosat="nancy"''',
        ]))
        self.assertEqual(
            [
                Token(tt.ELEMENT, 'testnames'),
                Token(tt.STR_ATTR, payload=('blah:', 'blah:'), make_safe=True),
                Token(tt.STR_ATTR, payload=('whosat', 'nancy'), make_safe=True),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_3(self):
        result = list(Tokenizer([
            '''~opentag''',
            '''    ~level_one''',
            '''        ~field @code: Code goes here''',
            ]))
        self.assertEqual(
            [
                Token(tt.ELEMENT, 'opentag'),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'level_one'),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'field'),
                Token(tt.STR_ATTR, ('name', 'code'), True),
                Token(tt.STR_DATA, 'Code goes here', make_safe=True),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_3_1(self):
        result = list(Tokenizer([
            '''!!!xml1.0''',
            '''~AccessRequest xml:lang="en-US"''',
            '''    ~AccessLicenseNumber: Your License Number''',
            '''    ~UserId: Your User ID''',
            '''    ~Password: Your Password''',
            ]))
        self.assertEqual(
            [
                Token(TokenType.META, payload=('xml', '1.0')),
                Token(tt.ELEMENT, 'AccessRequest'),
                Token(tt.STR_ATTR, ('xml:lang', 'en-US'), True),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'AccessLicenseNumber'),
                Token(tt.STR_DATA, payload=('Your License Number', )),
                Token(tt.ELEMENT, 'UserId'),
                Token(tt.STR_DATA, payload=('Your User ID', )),
                Token(tt.ELEMENT, 'Password'),
                Token(tt.STR_DATA, payload=('Your Password', )),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_3_2(self):
        result = list(Tokenizer([
            '''!!!xml1.0''',
            '''~AccessRequest xml:lang="en-US"''',
            '''    ~AccessLicenseNumber: Your License Number''',
            '''    ~UserId: Your User ID''',
            '''    ~Password: Your Password''',
            '''!!!xml1.0''',
            '''~TrackRequest xml:lang="en-US"''',
            '''    ~Request''',
            '''        ~TransactionReference''',
            '''            ~CustomerContext: Your Test Case Summary Description''',
            '''            ~XpciVersion: 1.0''',
            '''        ~RequestAction: Track''',
            '''        ~RequestOption: activity''',
            '''    ~TrackingNumber: Your Tracking Number''',
            ]))
        self.assertEqual(
            [
                Token(TokenType.META, payload=('xml', '1.0')),
                Token(tt.ELEMENT, 'AccessRequest'),
                Token(tt.STR_ATTR, ('xml:lang', 'en-US'), True),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'AccessLicenseNumber'),
                Token(tt.STR_DATA, payload=('Your License Number', )),
                Token(tt.ELEMENT, 'UserId'),
                Token(tt.STR_DATA, payload=('Your User ID', )),
                Token(tt.ELEMENT, 'Password'),
                Token(tt.STR_DATA, payload=('Your Password', )),
                Token(tt.DEDENT),

                Token(TokenType.META, payload=('xml', '1.0')),
                Token(tt.ELEMENT, 'TrackRequest'),
                Token(tt.STR_ATTR, ('xml:lang', 'en-US'), True),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'Request'),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'TransactionReference'),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'CustomerContext'),
                Token(tt.STR_DATA, 'Your Test Case Summary Description', make_safe=True),
                Token(tt.ELEMENT, 'XpciVersion'),
                Token(tt.STR_DATA, '1.0', make_safe=True),
                Token(tt.DEDENT),
                Token(tt.ELEMENT, 'RequestAction'),
                Token(tt.STR_DATA, 'Track', make_safe=True),
                Token(tt.ELEMENT, 'RequestOption'),
                Token(tt.STR_DATA, 'activity', make_safe=True),
                Token(tt.DEDENT),
                Token(tt.ELEMENT, 'TrackingNumber'),
                Token(tt.STR_DATA, 'Your Tracking Number', make_safe=True),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_4(self):
        result = list(Tokenizer([
            '''!!! xml''',
            '''-view="ir.ui.view"''',
            '''-model="some_test.my_table"''',
            '''~openerp''',
            '''  ~record #some_id model=view''',
            '''    @name: Folders''',
            '''    @arch type="xml"''',
        ]))
        self.assertEqual(
            [
                Token(TokenType.META, payload=('xml', '1.0')),
                Token(TokenType.PYTHON, payload=('view="ir.ui.view"',), make_safe=True),
                Token(TokenType.PYTHON, payload=('model="some_test.my_table"',), make_safe=True),
                Token(tt.ELEMENT, 'openerp'),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'record'),
                Token(tt.STR_ATTR, ('id', 'some_id'), True),
                Token(tt.CODE_ATTR, ('model', 'view'), True),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'field'),
                Token(tt.STR_ATTR, ('name', 'name'), True),
                Token(tt.STR_DATA, 'Folders', True),
                Token(tt.ELEMENT, 'field'),
                Token(tt.STR_ATTR, ('name', 'arch'), True),
                Token(tt.STR_ATTR, ('type', 'xml'), True),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_tokens_5(self):
        result = list(xaml.Tokenizer(([
            '''!!! xml''',
            '''~openerp''',
            '''   ~record #fax_id view="ui.ir.view"''',
            '''      @name: Folders''',
            '''      @arch type="xml"''',
            '''         ~form $Folders version="7.0"''',
            '''            ~group''',
            '''               ~group''',
            '''                  @id invisibility="1"''',
            '''                  @name''',
            '''                  @path''',
            '''               ~group''',
            '''                  @folder_type''',
        ])))
        self.assertEqual(
            [
                Token(TokenType.META, payload=('xml', '1.0')),
                Token(TokenType.ELEMENT, payload='openerp'),
                Token(TokenType.INDENT),
                Token(TokenType.ELEMENT, payload='record'),
                Token(TokenType.STR_ATTR, payload=('id', 'fax_id'), make_safe=True),
                Token(TokenType.STR_ATTR, payload=('view', 'ui.ir.view'), make_safe=True),
                Token(TokenType.INDENT),
                Token(TokenType.ELEMENT, payload='field'),
                Token(TokenType.STR_ATTR, payload=('name', 'name'), make_safe=True),
                Token(TokenType.STR_DATA, payload='Folders', make_safe=True),
                Token(TokenType.ELEMENT, payload='field'),
                Token(TokenType.STR_ATTR, payload=('name', 'arch'), make_safe=True),
                Token(TokenType.STR_ATTR, payload=('type', 'xml'), make_safe=True),
                Token(TokenType.INDENT),
                Token(TokenType.ELEMENT, payload='form'),
                Token(TokenType.STR_ATTR, payload=('string', 'Folders'), make_safe=True),
                Token(TokenType.STR_ATTR, payload=('version', '7.0'), make_safe=True),
                Token(TokenType.INDENT),
                Token(TokenType.ELEMENT, payload='group'),
                Token(TokenType.INDENT),
                Token(TokenType.ELEMENT, payload='group'),
                Token(TokenType.INDENT),
                Token(TokenType.ELEMENT, payload='field'),
                Token(TokenType.STR_ATTR, payload=('name', 'id'), make_safe=True),
                Token(TokenType.STR_ATTR, payload=('invisibility', '1'), make_safe=True),
                Token(TokenType.ELEMENT, payload='field'),
                Token(TokenType.STR_ATTR, payload=('name', 'name'), make_safe=True),
                Token(TokenType.ELEMENT, payload='field'),
                Token(TokenType.STR_ATTR, payload=('name', 'path'), make_safe=True),
                Token(TokenType.DEDENT),
                Token(TokenType.ELEMENT, payload='group'),
                Token(TokenType.INDENT),
                Token(TokenType.ELEMENT, payload='field'),
                Token(TokenType.STR_ATTR, payload=('name', 'folder_type'), make_safe=True),
                Token(TokenType.DEDENT),
                Token(TokenType.DEDENT),
                Token(TokenType.DEDENT),
                Token(TokenType.DEDENT),
                Token(TokenType.DEDENT),
                Token(TokenType.DEDENT),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_meta_token(self):
        result = list(xaml.Tokenizer(['!!! xml1.0',]))
        self.assertEqual(
            [
                Token(tt.META, ('xml', '1.0')),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_string_tokens(self):
        result = list(xaml.Tokenizer(['~test_tag $This_could_be_VERY_cool!',]))
        self.assertEqual(
            [
                Token(tt.ELEMENT, 'test_tag'),
                Token(tt.STR_ATTR, ('string', 'This could be VERY cool!'), True),
                Token(tt.DEDENT),
            ],
            result,
            )

    def test_code_data(self):
        result = list(xaml.Tokenizer(['~top_tag', '  ~record_tag', '    @Setting: = a_var']))
        self.assertEqual(
            [
                Token(tt.ELEMENT, 'top_tag'),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'record_tag'),
                Token(tt.INDENT),
                Token(tt.ELEMENT, 'field'),
                Token(tt.STR_ATTR, ('name', 'Setting'), True),
                Token(tt.CODE_DATA, 'a_var', make_safe=True),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
                Token(tt.DEDENT),
            ],
            result,
            )


class TestMultiDoc(TestCase):

    def test_xml_xml(self):
        input = (
            '''!!!xml1.0\n'''
            '''~items\n'''
            '''    ~item @id type='fields'\n'''
            '''        ~name @name type='field'\n'''
            '''        ~price @retail type='field'\n'''
            '''\n'''
            '''!!!xml1.0\n'''
            '''~xsl:stylesheet version='1.0'\n'''
            '''\n'''
            '''    ~xsl:template match='/'\n'''
            '''        ~xsl:apply-templates select='items'\n'''
            )
        xml1 = (
            '''<?xml version="1.0"?>\n'''
            '''<items>\n'''
            '''    <item name="id" type="fields">\n'''
            '''        <name name="name" type="field"/>\n'''
            '''        <price name="retail" type="field"/>\n'''
            '''    </item>\n'''
            '''</items>'''
            )
        xml2 = (
            '''<?xml version="1.0" encoding="utf-8"?>\n'''
            '''<xsl:stylesheet version="1.0">\n'''
            '''\n'''
            '''    <xsl:template match="/">\n'''
            '''        <xsl:apply-templates select="items"/>\n'''
            '''    </xsl:template>\n'''
            '''\n'''
            '''</xsl:stylesheet>'''
            ).encode('utf-8')
        doc = Xaml(input.encode('utf-8')).document
        self.assertEqual(len(doc.pages), 2)
        self.assertEqual([p.doc_type for p in doc.pages], ['xml', 'xml'])
        self.assertEqual(doc.pages[0].string(), xml1)
        self.assertEqual(doc.pages[1].bytes(), xml2)

    def test_xml_multi_root(self):
        input = (
            '''!!!xml1.0\n'''
            '''~items\n'''
            '''    ~item @id type='fields'\n'''
            '''        ~name @name type='field'\n'''
            '''        ~price @retail type='field'\n'''
            '''\n'''
            '''!!!xml1.0\n'''
            '''~stuffs xml:lang='en-US'\n'''
            '''    ~blah @id type='fields'\n'''
            '''        ~name @name type='field'\n'''
            '''        ~price @retail type='field'\n'''
            '''\n'''
            )
        xml1 = (
            '''<?xml version="1.0"?>\n'''
            '''<items>\n'''
            '''    <item name="id" type="fields">\n'''
            '''        <name name="name" type="field"/>\n'''
            '''        <price name="retail" type="field"/>\n'''
            '''    </item>\n'''
            '''</items>'''
            )
        xml2 = (
            '''<?xml version="1.0"?>\n'''
            '''<stuffs xml:lang="en-US">\n'''
            '''    <blah name="id" type="fields">\n'''
            '''        <name name="name" type="field"/>\n'''
            '''        <price name="retail" type="field"/>\n'''
            '''    </blah>\n'''
            '''</stuffs>'''
            )
        doc = Xaml(input.encode('utf-8')).document
        self.assertEqual(len(doc.pages), 2)
        self.assertEqual([p.doc_type for p in doc.pages], ['xml', 'xml'])
        self.assertEqual(doc.pages[0].string(), xml1)
        self.assertEqual(doc.pages[1].string(), xml2)

    def test_xml_xml_xml(self):
        input = (
            '''!!!xml1.0\n'''
            '''~items\n'''
            '''    ~item @id type='fields'\n'''
            '''        ~name @name type='field'\n'''
            '''        ~price @retail type='field'\n'''
            '''\n'''
            '''!!!xml1.0\n'''
            '''~stuffs xml:lang='en-US'\n'''
            '''    ~blah @id type='fields'\n'''
            '''        ~name @name type='field'\n'''
            '''        ~price @retail type='field'\n'''
            '''!!!xml1.0\n'''
            '''~more-stuffs xml:lang='en-US'\n'''
            '''    ~blah @id type='fields'\n'''
            '''        ~name @name type='field'\n'''
            '''        ~size @retail type='field'\n'''
            '''\n'''
            )
        xml1 = (
            '''<?xml version="1.0"?>\n'''
            '''<items>\n'''
            '''    <item name="id" type="fields">\n'''
            '''        <name name="name" type="field"/>\n'''
            '''        <price name="retail" type="field"/>\n'''
            '''    </item>\n'''
            '''</items>'''
            )
        xml2 = (
            '''<?xml version="1.0"?>\n'''
            '''<stuffs xml:lang="en-US">\n'''
            '''    <blah name="id" type="fields">\n'''
            '''        <name name="name" type="field"/>\n'''
            '''        <price name="retail" type="field"/>\n'''
            '''    </blah>\n'''
            '''</stuffs>'''
            )
        xml3 = (
            '''<?xml version="1.0"?>\n'''
            '''<more-stuffs xml:lang="en-US">\n'''
            '''    <blah name="id" type="fields">\n'''
            '''        <name name="name" type="field"/>\n'''
            '''        <size name="retail" type="field"/>\n'''
            '''    </blah>\n'''
            '''</more-stuffs>'''
            )
        doc = Xaml(input.encode('utf-8')).document
        self.assertEqual(len(doc.pages), 3)
        self.assertEqual([p.doc_type for p in doc.pages], ['xml', 'xml', 'xml'])
        self.assertEqual(doc.pages[0].string(), xml1)
        self.assertEqual(doc.pages[1].string(), xml2)
        self.assertEqual(doc.pages[2].string(), xml3)

    def test_xml_xsl(self):
        input = (
            '''!!!xml1.0\n'''
            '''~items\n'''
            '''    ~item @id type='fields'\n'''
            '''        ~name @name type='field'\n'''
            '''        ~price @retail type='field'\n'''
            '''\n'''
            '''!!!xsl1.0\n'''
            '''~xsl\n'''
            '''\n'''
            '''    ~xsl:template match='/'\n'''
            '''        ~xsl:apply-templates select='items'\n'''
            )
        xml = (
            '''<?xml version="1.0"?>\n'''
            '''<items>\n'''
            '''    <item name="id" type="fields">\n'''
            '''        <name name="name" type="field"/>\n'''
            '''        <price name="retail" type="field"/>\n'''
            '''    </item>\n'''
            '''</items>'''
            )
        xsl = (
            '''<?xml version="1.0"?>\n'''
            '''<xsl:stylesheet version="1.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n'''
            '''\n'''
            '''    <xsl:template match="/">\n'''
            '''        <xsl:apply-templates select="items"/>\n'''
            '''    </xsl:template>\n'''
            '''\n'''
            '''</xsl:stylesheet>'''
            )
        doc = Xaml(input.encode('utf-8')).document
        self.assertEqual(len(doc.pages), 2)
        self.assertEqual([p.doc_type for p in doc.pages], ['xml', 'xsl'])
        self.assertEqual(doc.pages[0].string(), xml)
        self.assertEqual(doc.pages[1].string(), xsl)

    # def test_html_html(self):
    #     raise NotImplementedError()

    # def test_html_css(self):
    #     raise NotImplementedError()


class TestMemoryLeak(TestCase):

    def test_multiple_iteration_sanity(self):
        res = {}
        template = Xaml(file_list).document.pages[0]
        for id in range(100000):
            res[id] = file_list * 50

    def test_multiple_iteration_real(self):
        res = {}
        for id in range(100000):
            template = Xaml(file_list).document.pages[0]
            website_download = 'blablah%d' % id
            leaf_path = 'haha_%d' % id
            web_folder = '%d-uhoh' % id
            display_files = ['this_%d' % id, 'that_%d' % id, 'these_%d' % id]
            safe_files = ['ths_%d' % id, 'tht_%d' % id, 'thse_%d' % id]
            website_select = '/some/stuff?model=yeahright-%d' % id
            perms = 'read'
            res[id] = template.string(
                    download=website_download,
                    path=leaf_path,
                    folder=web_folder,
                    display_files=display_files,
                    web_files=safe_files,
                    select=website_select,
                    permissions=perms,
                    )


file_list = '''
~div
    ~ul
        -for wfile, dfile in zip(args.web_files, args.display_files):
            -path = '%s?path=%s&folder=%s&file=%s' % (args.download, args.path, args.folder, wfile)
            ~li
                ~a href=path target='_blank': =dfile
    ~br
    -if args.permissions == 'write/unlink':
        ~a href=args.select target='_blank': Add/Delete files...
    -elif args.permissions == 'write':
        ~a href=args.select target='_blank': Add files...
    -elif args.permissions == 'unlink':
        ~a href=args.select target='_blank': Delete files...
'''


def xml2dict(line):
    if isinstance(line, bytes):
        line = line.decode('utf-8')
    blank, line = line.split('<')
    tag, attrs = line.split(' ', 1)
    attrs, end = attrs.rsplit('"', 1)
    result = {'blank':blank, 'tag':tag, 'end':end}
    for attr in attrs.split('" '):
        name, value = attr.split('="')
        result[name] = value
    return result


if __name__ == '__main__':
    main()
