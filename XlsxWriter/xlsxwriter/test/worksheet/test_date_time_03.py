###############################################################################
#
# Tests for XlsxWriter.
#
# Copyright (c), 2013-2014, John McNamara, jmcnamara@cpan.org
#

import unittest
import datetime
from ...worksheet import Worksheet


class TestConvertDateTime(unittest.TestCase):
    """
    Test the Worksheet _convert_date_time() method against dates extracted
    from Excel.

    """
    def setUp(self):
        self.worksheet = Worksheet()

        # Dates and corresponding numbers from an Excel file.
        self.excel_seconds = [
            ('00:00:00.000', 0),
            ('00:15:20.213', 1.0650613425925924E-2),
            ('00:16:48.290', 1.1670023148148148E-2),
            ('00:55:25.446', 3.8488958333333337E-2),
            ('01:02:46.891', 4.3598275462962965E-2),
            ('01:04:15.597', 4.4624965277777782E-2),
            ('01:09:40.889', 4.8389918981481483E-2),
            ('01:11:32.560', 4.9682407407407404E-2),
            ('01:30:19.169', 6.2721863425925936E-2),
            ('01:48:25.580', 7.5296064814814809E-2),
            ('02:03:31.919', 8.5786099537037031E-2),
            ('02:11:11.986', 9.1110949074074077E-2),
            ('02:24:37.095', 0.10042934027777778),
            ('02:35:07.220', 0.1077224537037037),
            ('02:45:12.109', 0.11472348379629631),
            ('03:06:39.990', 0.12962951388888888),
            ('03:08:08.251', 0.13065105324074075),
            ('03:19:12.576', 0.13833999999999999),
            ('03:29:42.574', 0.14563164351851851),
            ('03:37:30.813', 0.1510510763888889),
            ('04:14:38.231', 0.1768313773148148),
            ('04:16:28.559', 0.17810832175925925),
            ('04:17:58.222', 0.17914608796296297),
            ('04:21:41.794', 0.18173372685185185),
            ('04:56:35.792', 0.2059698148148148),
            ('05:25:14.885', 0.22586672453703704),
            ('05:26:05.724', 0.22645513888888891),
            ('05:46:44.068', 0.24078782407407406),
            ('05:48:01.141', 0.2416798726851852),
            ('05:53:52.315', 0.24574438657407408),
            ('06:14:48.580', 0.26028449074074073),
            ('06:46:15.738', 0.28212659722222222),
            ('07:31:20.407', 0.31343063657407405),
            ('07:58:33.754', 0.33233511574074076),
            ('08:07:43.130', 0.33869363425925925),
            ('08:29:11.091', 0.35360059027777774),
            ('09:08:15.328', 0.380732962962963),
            ('09:30:41.781', 0.39631690972222228),
            ('09:34:04.462', 0.39866275462962958),
            ('09:37:23.945', 0.40097158564814817),
            ('09:37:56.655', 0.40135017361111114),
            ('09:45:12.230', 0.40639155092592594),
            ('09:54:14.782', 0.41267108796296298),
            ('09:54:22.108', 0.41275587962962962),
            ('10:01:36.151', 0.41777952546296299),
            ('12:09:48.602', 0.50681252314814818),
            ('12:34:08.549', 0.52371005787037039),
            ('12:56:06.495', 0.53896406249999995),
            ('12:58:58.217', 0.54095158564814816),
            ('12:59:54.263', 0.54160026620370372),
            ('13:34:41.331', 0.56575614583333333),
            ('13:58:28.601', 0.58227547453703699),
            ('14:02:16.899', 0.58491781249999997),
            ('14:36:17.444', 0.60853523148148148),
            ('14:37:57.451', 0.60969271990740748),
            ('14:57:42.757', 0.6234115393518519),
            ('15:10:48.307', 0.6325035532407407),
            ('15:14:39.890', 0.63518391203703706),
            ('15:19:47.988', 0.63874986111111109),
            ('16:04:24.344', 0.66972620370370362),
            ('16:22:23.952', 0.68222166666666662),
            ('16:29:55.999', 0.6874536921296297),
            ('16:58:20.259', 0.70717892361111112),
            ('17:04:02.415', 0.71113906250000003),
            ('17:18:29.630', 0.72117627314814825),
            ('17:47:21.323', 0.74121901620370367),
            ('17:53:29.866', 0.74548456018518516),
            ('17:53:41.076', 0.74561430555555563),
            ('17:55:06.044', 0.74659773148148145),
            ('18:14:49.151', 0.760291099537037),
            ('18:17:45.738', 0.76233493055555546),
            ('18:29:59.700', 0.77082986111111118),
            ('18:33:21.233', 0.77316241898148153),
            ('19:14:24.673', 0.80167445601851861),
            ('19:17:12.816', 0.80362055555555545),
            ('19:23:36.418', 0.80806039351851855),
            ('19:46:25.908', 0.82391097222222232),
            ('20:07:47.314', 0.83874206018518516),
            ('20:31:37.603', 0.85529633101851854),
            ('20:39:57.770', 0.86108530092592594),
            ('20:50:17.067', 0.86825309027777775),
            ('21:02:57.827', 0.87705818287037041),
            ('21:23:05.519', 0.891036099537037),
            ('21:34:49.572', 0.89918486111111118),
            ('21:39:05.944', 0.90215212962962965),
            ('21:39:18.426', 0.90229659722222222),
            ('21:46:07.769', 0.90703436342592603),
            ('21:57:55.662', 0.91522756944444439),
            ('22:19:11.732', 0.92999689814814823),
            ('22:23:51.376', 0.93323351851851843),
            ('22:27:58.771', 0.93609688657407408),
            ('22:43:30.392', 0.94687953703703709),
            ('22:48:25.834', 0.95029900462962968),
            ('22:53:51.727', 0.95407091435185187),
            ('23:12:56.536', 0.96732101851851848),
            ('23:15:54.109', 0.96937626157407408),
            ('23:17:12.632', 0.97028509259259266),
            ('23:59:59.999', 0.99999998842592586),
        ]

        # Dates and corresponding numbers from an Excel file.
        self.excel_dates = [
            ('1899-12-31T00:00:00.000', 0),
            ('1899-12-31T00:15:20.213', 1.0650613425925924E-2),
            ('1899-12-31T00:16:48.290', 1.1670023148148148E-2),
            ('1899-12-31T00:55:25.446', 3.8488958333333337E-2),
            ('1899-12-31T01:02:46.891', 4.3598275462962965E-2),
            ('1899-12-31T01:04:15.597', 4.4624965277777782E-2),
            ('1899-12-31T01:09:40.889', 4.8389918981481483E-2),
            ('1899-12-31T01:11:32.560', 4.9682407407407404E-2),
            ('1899-12-31T01:30:19.169', 6.2721863425925936E-2),
            ('1899-12-31T01:48:25.580', 7.5296064814814809E-2),
            ('1899-12-31T02:03:31.919', 8.5786099537037031E-2),
            ('1899-12-31T02:11:11.986', 9.1110949074074077E-2),
            ('1899-12-31T02:24:37.095', 0.10042934027777778),
            ('1899-12-31T02:35:07.220', 0.1077224537037037),
            ('1899-12-31T02:45:12.109', 0.11472348379629631),
            ('1899-12-31T03:06:39.990', 0.12962951388888888),
            ('1899-12-31T03:08:08.251', 0.13065105324074075),
            ('1899-12-31T03:19:12.576', 0.13833999999999999),
            ('1899-12-31T03:29:42.574', 0.14563164351851851),
            ('1899-12-31T03:37:30.813', 0.1510510763888889),
            ('1899-12-31T04:14:38.231', 0.1768313773148148),
            ('1899-12-31T04:16:28.559', 0.17810832175925925),
            ('1899-12-31T04:17:58.222', 0.17914608796296297),
            ('1899-12-31T04:21:41.794', 0.18173372685185185),
            ('1899-12-31T04:56:35.792', 0.2059698148148148),
            ('1899-12-31T05:25:14.885', 0.22586672453703704),
            ('1899-12-31T05:26:05.724', 0.22645513888888891),
            ('1899-12-31T05:46:44.068', 0.24078782407407406),
            ('1899-12-31T05:48:01.141', 0.2416798726851852),
            ('1899-12-31T05:53:52.315', 0.24574438657407408),
            ('1899-12-31T06:14:48.580', 0.26028449074074073),
            ('1899-12-31T06:46:15.738', 0.28212659722222222),
            ('1899-12-31T07:31:20.407', 0.31343063657407405),
            ('1899-12-31T07:58:33.754', 0.33233511574074076),
            ('1899-12-31T08:07:43.130', 0.33869363425925925),
            ('1899-12-31T08:29:11.091', 0.35360059027777774),
            ('1899-12-31T09:08:15.328', 0.380732962962963),
            ('1899-12-31T09:30:41.781', 0.39631690972222228),
            ('1899-12-31T09:34:04.462', 0.39866275462962958),
            ('1899-12-31T09:37:23.945', 0.40097158564814817),
            ('1899-12-31T09:37:56.655', 0.40135017361111114),
            ('1899-12-31T09:45:12.230', 0.40639155092592594),
            ('1899-12-31T09:54:14.782', 0.41267108796296298),
            ('1899-12-31T09:54:22.108', 0.41275587962962962),
            ('1899-12-31T10:01:36.151', 0.41777952546296299),
            ('1899-12-31T12:09:48.602', 0.50681252314814818),
            ('1899-12-31T12:34:08.549', 0.52371005787037039),
            ('1899-12-31T12:56:06.495', 0.53896406249999995),
            ('1899-12-31T12:58:58.217', 0.54095158564814816),
            ('1899-12-31T12:59:54.263', 0.54160026620370372),
            ('1899-12-31T13:34:41.331', 0.56575614583333333),
            ('1899-12-31T13:58:28.601', 0.58227547453703699),
            ('1899-12-31T14:02:16.899', 0.58491781249999997),
            ('1899-12-31T14:36:17.444', 0.60853523148148148),
            ('1899-12-31T14:37:57.451', 0.60969271990740748),
            ('1899-12-31T14:57:42.757', 0.6234115393518519),
            ('1899-12-31T15:10:48.307', 0.6325035532407407),
            ('1899-12-31T15:14:39.890', 0.63518391203703706),
            ('1899-12-31T15:19:47.988', 0.63874986111111109),
            ('1899-12-31T16:04:24.344', 0.66972620370370362),
            ('1899-12-31T16:22:23.952', 0.68222166666666662),
            ('1899-12-31T16:29:55.999', 0.6874536921296297),
            ('1899-12-31T16:58:20.259', 0.70717892361111112),
            ('1899-12-31T17:04:02.415', 0.71113906250000003),
            ('1899-12-31T17:18:29.630', 0.72117627314814825),
            ('1899-12-31T17:47:21.323', 0.74121901620370367),
            ('1899-12-31T17:53:29.866', 0.74548456018518516),
            ('1899-12-31T17:53:41.076', 0.74561430555555563),
            ('1899-12-31T17:55:06.044', 0.74659773148148145),
            ('1899-12-31T18:14:49.151', 0.760291099537037),
            ('1899-12-31T18:17:45.738', 0.76233493055555546),
            ('1899-12-31T18:29:59.700', 0.77082986111111118),
            ('1899-12-31T18:33:21.233', 0.77316241898148153),
            ('1899-12-31T19:14:24.673', 0.80167445601851861),
            ('1899-12-31T19:17:12.816', 0.80362055555555545),
            ('1899-12-31T19:23:36.418', 0.80806039351851855),
            ('1899-12-31T19:46:25.908', 0.82391097222222232),
            ('1899-12-31T20:07:47.314', 0.83874206018518516),
            ('1899-12-31T20:31:37.603', 0.85529633101851854),
            ('1899-12-31T20:39:57.770', 0.86108530092592594),
            ('1899-12-31T20:50:17.067', 0.86825309027777775),
            ('1899-12-31T21:02:57.827', 0.87705818287037041),
            ('1899-12-31T21:23:05.519', 0.891036099537037),
            ('1899-12-31T21:34:49.572', 0.89918486111111118),
            ('1899-12-31T21:39:05.944', 0.90215212962962965),
            ('1899-12-31T21:39:18.426', 0.90229659722222222),
            ('1899-12-31T21:46:07.769', 0.90703436342592603),
            ('1899-12-31T21:57:55.662', 0.91522756944444439),
            ('1899-12-31T22:19:11.732', 0.92999689814814823),
            ('1899-12-31T22:23:51.376', 0.93323351851851843),
            ('1899-12-31T22:27:58.771', 0.93609688657407408),
            ('1899-12-31T22:43:30.392', 0.94687953703703709),
            ('1899-12-31T22:48:25.834', 0.95029900462962968),
            ('1899-12-31T22:53:51.727', 0.95407091435185187),
            ('1899-12-31T23:12:56.536', 0.96732101851851848),
            ('1899-12-31T23:15:54.109', 0.96937626157407408),
            ('1899-12-31T23:17:12.632', 0.97028509259259266),
            ('1899-12-31T23:59:59.999', 0.99999998842592586),
        ]

    def test_convert_date_time(self):
        """Test the _convert_date_time() method for seconds."""

        for excel_date in self.excel_dates:
            date = datetime.datetime.strptime(excel_date[0], "%Y-%m-%dT%H:%M:%S.%f")

            got = self.worksheet._convert_date_time(date)
            exp = excel_date[1]

            self.assertAlmostEqual(got, exp, places=15)

    def test_convert_date_time_seconds_only(self):
        """Test the _convert_date_time() method for datetime seconds."""

        for excel_date in self.excel_seconds:
            date = datetime.datetime.strptime(excel_date[0], "%H:%M:%S.%f")

            got = self.worksheet._convert_date_time(date)
            exp = excel_date[1]

            self.assertAlmostEqual(got, exp, places=15)

    def test_convert_date_time_seconds_only_time(self):
        """Test the _convert_date_time() method for time seconds."""

        for excel_date in self.excel_seconds:
            date = datetime.datetime.strptime(excel_date[0], "%H:%M:%S.%f")

            time = datetime.time(date.hour, date.minute, date.second, date.microsecond)

            got = self.worksheet._convert_date_time(time)
            exp = excel_date[1]

            self.assertAlmostEqual(got, exp, places=15)
