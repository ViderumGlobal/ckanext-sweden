from pylons import config
from nose import tools as nosetools
try:
    import ckan.tests.factories as factories
    import ckan.tests.helpers as helpers
except ImportError:
    # CKAN 2.3
    import ckan.new_tests.factories as factories
    import ckan.new_tests.helpers as helpers


class TestDcatOrganizationList(helpers.FunctionalTestBase):

    def test_dcat_organization_list_no_orgs(self):
        '''
        dcat_organization_list action returns empty results when no orgs
        exists.
        '''
        dcat_org_list = helpers.call_action('dcat_organization_list')
        nosetools.assert_equal(dcat_org_list, [])

    def test_dcat_organization_list_has_keys(self):
        '''
        dcat_organization_list action returns list with the correct keys.
        '''
        org = factories.Organization(uri='http://example.com/uri')
        factories.Dataset(owner_org=org['id'],
                          type="harvest",
                          url="http://example.com/source")
        dcat_org_list = helpers.call_action('dcat_organization_list')

        nosetools.assert_equal(len(dcat_org_list), 1)
        org = dcat_org_list[0]
        nosetools.assert_true('uri' in org)
        nosetools.assert_true('original_dcat_metadata_url' in org)
        nosetools.assert_true('id' in org)
        nosetools.assert_true('dcat_metadata_url' in org)

    def test_dcat_organization_list_org_has_correct_values(self):
        '''
        dcat_organization_list action returns list of one result with correct
        values.
        '''
        org = factories.Organization(uri='http://example.com/uri')
        factories.Dataset(owner_org=org['id'],
                          type="harvest",
                          url="http://example.com/source")
        dcat_org_list = helpers.call_action('dcat_organization_list')

        nosetools.assert_equal(len(dcat_org_list), 1)
        dcat_org = dcat_org_list[0]
        nosetools.assert_equal(dcat_org['id'], org['id'])
        nosetools.assert_equal(dcat_org['original_dcat_metadata_url'], u'http://example.com/source')
        nosetools.assert_equal(dcat_org['uri'], u'http://example.com/uri')
        nosetools.assert_equal(dcat_org['dcat_metadata_url'],
                               '{0}/organization/{1}/dcat.rdf'.format(
                                   config.get('ckan.site_url').rstrip('/'),
                                   org['name']))

    def test_dcat_organization_list_no_orgs_without_harvest_pair(self):
        '''
        dcat_organization_list shouldn't list orgs that don't have a
        counterpart harvest dataset.
        '''
        factories.Organization()
        dcat_org_list = helpers.call_action('dcat_organization_list')

        nosetools.assert_equal(len(dcat_org_list), 0)