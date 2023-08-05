"""InVEST NDR model tests."""
import collections
import unittest
import tempfile
import shutil
import os

import numpy
from osgeo import ogr

REGRESSION_DATA = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'invest-test-data', 'ndr')


class NDRTests(unittest.TestCase):
    """Regression tests for InVEST SDR model."""

    def setUp(self):
        """Initalize SDRRegression tests."""
        self.workspace_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up remaining files."""
        shutil.rmtree(self.workspace_dir)

    @staticmethod
    def generate_base_args(workspace_dir):
        """Generate a base sample args dict for NDR."""
        args = {
            'biophysical_table_path':
            os.path.join(REGRESSION_DATA, 'input', 'biophysical_table.csv'),
            'calc_n': True,
            'calc_p': True,
            'dem_path': os.path.join(REGRESSION_DATA, 'input', 'dem.tif'),
            'k_param': 2.0,
            'lulc_path':
            os.path.join(REGRESSION_DATA, 'input', 'landuse_90.tif'),
            'runoff_proxy_path':
            os.path.join(REGRESSION_DATA, 'input', 'precip.tif'),
            'subsurface_critical_length_n': 150,
            'subsurface_critical_length_p': '150',
            'subsurface_eff_n': 0.4,
            'subsurface_eff_p': '0.8',
            'threshold_flow_accumulation': '1000',
            'watersheds_path':
            os.path.join(REGRESSION_DATA, 'input', 'watersheds.shp'),
            'workspace_dir': workspace_dir,
        }
        return args.copy()

    def test_missing_headers(self):
        """NDR biphysical headers missing should raise a ValueError."""
        from natcap.invest.ndr import ndr

        # use predefined directory so test can clean up files during teardown
        args = NDRTests.generate_base_args(self.workspace_dir)
        # make args explicit that this is a base run of SWY
        args['biophysical_table_path'] = os.path.join(
            REGRESSION_DATA, 'input', 'biophysical_table_missing_headers.csv')
        with self.assertRaises(ValueError):
            ndr.execute(args)

    def test_missing_lucode(self):
        """NDR missing lucode in biophysical table should raise a KeyError."""
        from natcap.invest.ndr import ndr

        # use predefined directory so test can clean up files during teardown
        args = NDRTests.generate_base_args(self.workspace_dir)
        # make args explicit that this is a base run of SWY
        args['biophysical_table_path'] = os.path.join(
            REGRESSION_DATA, 'input', 'biophysical_table_missing_lucode.csv')
        with self.assertRaises(KeyError):
            ndr.execute(args)

    def test_no_nutrient_selected(self):
        """NDR no nutrient selected should raise a ValueError."""
        from natcap.invest.ndr import ndr

        # use predefined directory so test can clean up files during teardown
        args = NDRTests.generate_base_args(self.workspace_dir)
        # make args explicit that this is a base run of SWY
        args['calc_n'] = False
        args['calc_p'] = False
        with self.assertRaises(ValueError):
            ndr.execute(args)

    def test_base_regression(self):
        """NDR base regression test on sample data.

        Execute NDR with sample data and checks that the output files are
        generated and that the aggregate shapefile fields are the same as the
        regression case.
        """
        from natcap.invest.ndr import ndr

        # use predefined directory so test can clean up files during teardown
        args = NDRTests.generate_base_args(self.workspace_dir)

        # make an empty output shapefile on top of where the new output
        # shapefile should reside to ensure the model overwrites it
        with open(
                os.path.join(self.workspace_dir, 'watershed_results_ndr.shp'),
                'wb') as f:
            f.write('')

        # make args explicit that this is a base run of SWY
        ndr.execute(args)

        NDRTests._assert_regression_results_equal(
            args['workspace_dir'],
            os.path.join(args['workspace_dir'], 'watershed_results_ndr.shp'),
            os.path.join(REGRESSION_DATA, 'agg_results_base.csv'))

    def test_validation(self):
        """NDR test argument validation."""
        from natcap.invest.ndr import ndr

        # use predefined directory so test can clean up files during teardown
        args = NDRTests.generate_base_args(self.workspace_dir)
        # should not raise an exception
        ndr.validate(args)

        with self.assertRaises(KeyError)  as context:
            del args['workspace_dir']
            ndr.validate(args)
        self.assertTrue(
            'The following keys were expected' in str(context.exception))

        args = NDRTests.generate_base_args(self.workspace_dir)
        args['workspace_dir'] = ''
        validation_error_list = ndr.validate(args)
        # we should have one warning that is an empty value
        self.assertEqual(len(validation_error_list), 1)

        # here the wrong GDAL type happens (vector instead of raster)
        args = NDRTests.generate_base_args(self.workspace_dir)
        args['lulc_path'] = args['watersheds_path']
        validation_error_list = ndr.validate(args)
        # we should have one warning that is an empty value
        self.assertEqual(len(validation_error_list), 1)

        # here the wrong GDAL type happens (raster instead of vector)
        args = NDRTests.generate_base_args(self.workspace_dir)
        args['watersheds_path'] = args['lulc_path']
        validation_error_list = ndr.validate(args)
        # we should have one warning that is an empty value
        self.assertEqual(len(validation_error_list), 1)

        # cover that there's no p and n calculation
        args = NDRTests.generate_base_args(self.workspace_dir)
        args['calc_p'] = False
        args['calc_n'] = False
        validation_error_list = ndr.validate(args)
        # we should have one warning that is an empty value
        self.assertEqual(len(validation_error_list), 1)

        # cover that a file is missing
        args = NDRTests.generate_base_args(self.workspace_dir)
        args['lulc_path'] = 'this/path/does/not/exist.tif'
        validation_error_list = ndr.validate(args)
        # we should have one warning that is an empty value
        self.assertEqual(len(validation_error_list), 1)


    @staticmethod
    def _assert_regression_results_equal(
            workspace_dir, result_vector_path, agg_results_path):
        """Test workspace state against expected aggregate results.

        Parameters:
            workspace_dir (string): path to the completed model workspace
            result_vector_path (string): path to the summary shapefile
                produced by the SWY model.
            agg_results_path (string): path to a csv file that has the
                expected aggregated_results.shp table in the form of
                fid,p_load_tot,p_exp_tot,n_load_tot,n_exp_tot per line

        Returns:
            None

        Raises:
            AssertionError if any files are missing or results are out of
            range by `tolerance_places`
        """
        # we expect a file called 'aggregated_results.shp'
        result_vector = ogr.Open(result_vector_path)
        result_layer = result_vector.GetLayer()

        error_results = collections.defaultdict(dict)
        with open(agg_results_path, 'rb') as agg_result_file:
            for line in agg_result_file:
                (fid, surf_p_ld, sub_p_ld, p_exp_tot,
                 surf_n_ld, sub_n_ld, n_exp_tot) = [
                    float(x) for x in line.split(',')]
                feature = result_layer.GetFeature(int(fid))
                if not feature:
                    raise AssertionError("The fid %s is missing." % fid)
                for field, value in [
                                    ('ws_id', fid),
                                    ('surf_p_ld', surf_p_ld),
                                    ('sub_p_ld', sub_p_ld),
                                    ('p_exp_tot', p_exp_tot),
                                    ('surf_n_ld', surf_n_ld),
                                    ('sub_n_ld', sub_n_ld),
                                    ('n_exp_tot', n_exp_tot)]:
                    if not numpy.isclose(feature.GetField(field), value):
                        error_results[fid][field] = (
                            feature.GetField(field), value)
                ogr.Feature.__swig_destroy__(feature)
                feature = None
        result_layer = None
        ogr.DataSource.__swig_destroy__(result_vector)
        result_vector = None
        if error_results:
            raise AssertionError(
                "The following values are not equal: %s" % error_results)
