from temci.report.report import ReporterRegistry
from temci.report.rundata import RunDataStatsHelper

class ReportProcessor:

    def __init__(self, stats_helper: RunDataStatsHelper = None):
        self.reporter = ReporterRegistry.get_for_name(ReporterRegistry.get_used(), stats_helper)

    def report(self):
        self.reporter.report()