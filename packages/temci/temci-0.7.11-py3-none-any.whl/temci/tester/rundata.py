"""
Contains the RunData object for benchmarking data of specific program block
and the RunDataStatsHelper that provides helper methods for working with
these objects.
"""

from temci.report.testers import Tester, TesterRegistry
from temci.utils.typecheck import *
from temci.utils.settings import Settings
import temci.utils.util as util
if util.can_import("scipy"):
    import scipy
import typing as t


class RunData(object):
    """
    A set of benchmarking data for a specific program block.
    """

    def __init__(self, data: t.Dict[str, t.List[t.Union[int, float]]] = None, attributes: t.Dict[str, str] = None,
                 external: bool = False):
        """
        Initializes a new run data object with a list of measured properties,
        an optional dictionary mapping each property to a list of actual values and
        a dictionary of optional attributes that describe its program block.
        """
        typecheck(data, E(None) | Dict(all_keys=False))
        typecheck(attributes, Exact(None) | Dict(key_type=Str(), all_keys=False))
        self.external = external
        self.properties = [] # type: t.List[str]
        """ List of measured properties. They might not all be measured the same number of times. """
        self.data = {} # type: t.Dict[str, t.List[t.Union[int, float]]]
        """ Raw benchmarking data, mapping properties to their corresponding values """
        if data is not None and len(data) > 0:
            self.add_data_block(data)
        self.attributes = attributes or {} # type: t.Dict[str, str]

    def add_data_block(self, data_block: t.Dict[str, t.List[t.Union[int, float]]]):
        """
        Adds a block of data. The passed dictionary maps each of the run datas properties to list of
        actual values (from each benchmarking run).
        """
        typecheck(data_block, Dict(key_type=Str(), value_type= List(Int() | Float()), all_keys=False))
        self.properties = set(self.properties).union(set(data_block.keys()))
        for prop in data_block:
            if prop not in self.data:
                self.data[prop] = []
                self.properties.add(prop)
            self.data[prop].extend(data_block[prop])
        self.properties = sorted(list(self.properties))

    def __len__(self) -> int:
        """
        Returns the number of measured properties.
        """
        return len(self.data)

    def min_values(self) -> int:
        """
        Returns the minimum number of measured values for the associated program block
        over all properties.
        """
        return min(map(len, self.data.values())) if len(self) > 0 else 0

    def benchmarks(self) -> int:
        """
        Returns the maximum number of measured values for the associated program block
        over all properties. This number should be equivalent to the number of measured
        benchmarking runs.
        """
        return max(map(len, self.data.values())) if len(self) > 0 else 0


    def __getitem__(self, property: str):
        """
        Returns the benchmarking values associated with the passed property.
        """
        return self.data[property]

    def to_dict(self) -> dict:
        """
        Returns a dictionary that represents this run data object.
        """
        return {
            "attributes": self.attributes,
            "data": self.data
        }

    def __str__(self):
        return repr(self.attributes)

    def description(self):
        if "description" in self.attributes:
            return self.attributes["description"]
        return ", ".join("{}={}".format(key, self.attributes[key]) for key in self.attributes)


class RunDataStatsHelper(object):
    """
    This class helps to simplify the work with a set of run data observations.
    """

    def __init__(self, runs: t.List[RunData], tester: Tester = None, external_count: int = 0):
        """
        Don't use the constructor use init_from_dicts if possible.
        :param runs: list of run data objects
        :param tester: used tester or tester that is set in the settings
        """
        self.tester = tester or TesterRegistry.get_for_name(TesterRegistry.get_used(),
                                                            Settings()["stats/uncertainty_range"])
        typecheck(runs, List(T(RunData)))
        self.runs = runs # type: t.List[RunData]
        self.external_count = external_count

    def properties(self) -> t.List[str]:
        """
        Returns a sorted list of all properties that exist in all (!) run data blocks.
        """
        if not self.runs:
            return []
        props = set(self.runs[0].properties)
        for rd in self.runs[1:]:
            if rd:
                props = props.intersection(rd.properties)
        return list(sorted(props))

    @classmethod
    def init_from_dicts(cls, runs: t.List[Dict] = None, external: bool = False) -> 'RunDataStatsHelper':
        """
        Expected structure of the stats settings and the runs parameter::

            "stats": {
                "tester": ...,
                "properties": ["prop1", ...],
                # or
                "properties": [("prop1", "description of prop1"), ...],
                "uncertainty_range": (0.1, 0.3)
            }

            "runs": [
                {"attributes": {"attr1": ..., ...},
                 "data": {"__ov-time": [...], ...}},
                 ...
            ]


        :param runs: list of dictionaries representing the benchmarking runs for each program block
        :param external: are the passed runs not from this benchmarking run but from another?
        :rtype RunDataStatsHelper
        :raises ValueError if the stats of the runs parameter have not the correct structure
        """
        typecheck(runs, List(Dict({
                    "data": Dict(key_type=Str(), value_type=List(Int()|Float()), all_keys=False) | NonExistent(),
                    "attributes": Dict(key_type=Str(), all_keys=False)
                }, all_keys=False)),
                value_name="runs parameter")
        run_datas = []
        runs = runs or [] # type: t.List[dict]
        for run in runs:
            if "data" not in run:
                run["data"] = {}
            run_datas.append(RunData(run["data"], run["attributes"], external=external))
        return RunDataStatsHelper(run_datas, external_count=len(runs) if external else 0)

    def _is_uncertain(self, property: str, data1: RunData, data2: RunData) -> bool:
        return self.tester.is_uncertain(data1[property], data2[property])

    def _is_equal(self, property: str, data1: RunData, data2: RunData) -> bool:
        return self.tester.is_equal(data1[property], data2[property])

    def _is_unequal(self, property: str, data1: RunData, data2: RunData) -> bool:
        return self.tester.is_unequal(data1[property], data2[property])

    def is_uncertain(self, p_val: float) -> bool:
        return min(*Settings()["stats/uncertainty_range"]) <= p_val <= max(*Settings()["stats/uncertainty_range"])

    def is_equal(self, p_val: float) -> bool:
        return p_val > max(*Settings()["stats/uncertainty_range"])

    def is_unequal(self, p_val: float) -> bool:
        return p_val < min(*Settings()["stats/uncertainty_range"])

    def _speed_up(self, property: str, data1: RunData, data2: RunData):
        """
        Calculates the speed up from the second to the first
        (e.g. the first is RESULT * 100 % faster than the second).
        """
        return (scipy.mean(data2[property]) - scipy.mean(data1[property])) \
               / scipy.mean(data1[property])

    def _estimate_time_for_run_datas(self, run_bin_size: int, data1: RunData, data2: RunData,
                                     min_runs: int, max_runs: int) -> float:
        if min(len(data1), len(data2)) == 0 or "__ov-time" not in data1.properties or "__ov-time" not in data2.properties:
            return max_runs
        needed_runs = []
        for prop in set(data1.properties).intersection(data2.properties):
            estimate = self.tester.estimate_needed_runs(data1[prop], data2[prop],
                                                                run_bin_size, min_runs, max_runs)
            needed_runs.append(estimate)
        avg_time = max(scipy.mean(data1["__ov-time"]), scipy.mean(data2["__ov-time"]))
        return max(needed_runs) * avg_time

    def get_program_ids_to_bench(self) -> t.List[int]:
        """
        Returns the ids (the first gets id 0, …) of the program block / run data object that
        should be benchmarked again.
        """
        to_bench = set()
        for (i, run) in enumerate(self.runs):
            if i in to_bench or not run:
                continue
            for j in range(i):
                if j in to_bench or not self.runs[j]:
                    continue
                run2 = self.runs[j]
                if any(self._is_uncertain(prop, run, run2) for prop in set(run.properties)
                        .intersection(run2.properties)):
                    to_bench.add(i)
                    to_bench.add(j)
        return [i - self.external_count for i in to_bench if i >= self.external_count]

    def estimate_time(self, run_bin_size: int, min_runs: int, max_runs: int) -> float:
        """
        Roughly erstimates the time needed to finish benchmarking all program blocks.
        It doesn't take any parallelism into account. Therefore divide the number by the used parallel processes.
        :param run_bin_size: times a program block is benchmarked in a single block of time
        :param min_runs: minimum number of allowed runs
        :param max_runs: maximum number of allowed runs
        :return estimated time in seconds or float("inf") if no proper estimation could be made
        """
        to_bench = self.get_program_ids_to_bench()
        max_times = [0 for i in self.runs]
        for i in to_bench:
            run = self.runs[i]
            for j in to_bench:
                max_time = self._estimate_time_for_run_datas(run_bin_size, run, self.runs[j],
                                                             min_runs, max_runs)
                max_times[i] = max(max_times[i], max_time)
                max_times[j] = max(max_times[j], max_time)
                if max_time == float("inf"):
                    return float("inf")
        return sum(max_times)

    def estimate_time_for_next_round(self, run_bin_size: int, all: bool) -> float:
        """
        Roughly estimates the time needed for the next benchmarking round.
        :param run_bin_size: times a program block is benchmarked in a single block of time and the size of a round
        :param all: expect all program block to be benchmarked
        :return estimated time in seconds
        """
        if "__ov-time" not in self.properties():
            return -1
        summed = 0
        to_bench = range(0, len(self.runs)) if all else self.get_program_ids_to_bench()
        for i in to_bench:
            summed += scipy.mean(self.runs[i]["__ov-time"]) * run_bin_size
        return summed

    def add_run_data(self, data: list = None, attributes: dict = None) -> int:
        """
        Adds a new run data (corresponding to a program block) and returns its id.
        :param data: benchmarking data of the new run data object
        :param attributes: attributes of the new run data object
        :return: id of the run data object (and its corresponding program block)
        """
        self.runs.append(RunData(self.properties, data, attributes))
        return len(self.runs) - 1

    def disable_run_data(self, id: int):
        """
        Disable that run data object with the given id.
        """
        self.runs[id] = None

    def add_data_block(self, program_id: int, data_block: t.Dict[str, t.List[t.Union[int, float]]]):
        """
        Add block of data for the program block with the given id.
        :param program_id: id of the program.
        :param data_block: list of data from several benchmarking runs of the program block
        :raises ValueError if the program block with the given id doesn't exist
        """
        program_id += self.external_count
        assert program_id >= self.external_count
        if program_id >= len(self.runs):
            raise ValueError("Program block with id {} doesn't exist".format(program_id - self.external_count))
        self.runs[program_id].add_data_block(data_block)

    def get_evaluation(self, with_equal: bool, with_unequal: bool, with_uncertain: bool) -> dict:
        """

        Structure of the returned list items::

            - data: # set of two run data objects
              properties: # information for each property that is equal, ...
                  -prop:
                      - equal: True/False
                        uncertain: True/False
                        p_val: probability of the null hypothesis
                        speed_up: speed up from the first to the second
                        description: description of the property

        :param with_equal: with tuple with at least one "equal" property
        :param with_unequal: ... unequal property
        :param with_uncertain: include also uncertain properties
        :return: list of tuples for which at least one property matches the criteria
        """
        arr = []
        for i in range(0, len(self.runs) - 1):
            for j in range(i + 1, len(self.runs)):
                if not self.runs[i] or not self.runs[j]:
                    continue
                data = (self.runs[i], self.runs[j])
                props = {}
                for prop in self.properties():
                    map = {"p_val": self.tester.test(data[0][prop], data[1][prop]),
                           "speed_up": self._speed_up(prop, *data),
                           "description": prop,
                           "equal": self._is_equal(prop, *data),
                           "unequal": self._is_unequal(prop, *data),
                           "uncertain": self._is_uncertain(prop, *data)}
                    if map["unequal"] == with_unequal and map["equal"] == with_equal \
                            and map["uncertain"] == with_uncertain:
                        props[prop] = map
                if len(props) > 0:
                    arr.append({
                        "data": data,
                        "properties": props
                    })
        return arr

    def serialize(self) -> t.List:
        return list(x.to_dict() for x in self.runs if x)

    def valid_runs(self) -> t.List[RunData]:
        res = [x for x in self.runs if x is not None]
        #print(res)
        return res