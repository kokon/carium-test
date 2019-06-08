"""
#
# Example custom-job code
#
# Copyright(c) 2019, Carium, Inc. All rights reserved.
#
"""

import csv
import json
import sys

import altair as alt

from cariutils.typing import JsonDict
from cronkite.custom_job.framework.base import JobV1


class MyJob(JobV1):

    def on_report(self) -> str:
        print("Debugging...")
        print('Error', file=sys.stderr)

        filename = self._get_workfile('test.csv')
        with open(filename, 'w', newline='') as fout:
            writer = csv.writer(fout)
            writer.writerow(['x', 'y', 'z'])
            for i in range(1, 4):
                writer.writerow([str(i * 1), str(i * 2), str(i * 3)])

        return filename

    def on_view(self, file) -> JsonDict:
        reader = csv.DictReader(file)
        data = alt.Data(values=list(reader))
        return json.loads(alt.Chart(data).mark_bar().encode(
            x='x:O',  # specify ordinal data
            y='y:Q',  # specify quantitative data
        ).to_json())
