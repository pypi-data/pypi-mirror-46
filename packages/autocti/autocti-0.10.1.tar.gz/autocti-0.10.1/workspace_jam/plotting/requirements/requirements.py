
import matplotlib.pyplot as plt

from workspace_jam.plotting.requirements import parallel_x2_requirements
from workspace_jam.plotting.requirements import parallel_x3_requirements
from workspace_jam.plotting.requirements import serial_x2_requirements

import os

# Setup the path to the workspace, using a relative directory name.
workspace_path = '{}/../../'.format(os.path.dirname(os.path.realpath(__file__)))
plot_path = '{}/plotting/requirements/plots/'.format(workspace_path)
output_path = workspace_path + '../../outputs/PyAutoCTI/'

ci_resolutions = ['low_resolution', 'mid_resolution', 'high_resolution']

requirement_means_parallel_x2, requirement_errors_parallel_x2 = \
    parallel_x2_requirements.parallel_x2_requirements_of_resolutions(ci_resolutions=ci_resolutions)

# requirement_means_parallel_x3, requirement_errors_parallel_x3 = \
#     parallel_x3_requirements.parallel_x3_requirements_of_resolutions(ci_resolutions=ci_resolutions)

requirement_means_serial_x2, requirement_errors_serial_x2 = \
    serial_x2_requirements.serial_x2_requirements_of_resolutions(ci_resolutions=ci_resolutions)

columns = [517, 1034, 2068]#, 4136]

plt.figure(figsize=(20, 15))
plt.suptitle('Requirements for CTI Models', fontsize=20)

eb0 = plt.errorbar(x=columns, y=requirement_means_parallel_x2,
                  yerr=[requirement_errors_parallel_x2, requirement_errors_parallel_x2],
                  capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb0[-1][0].set_linestyle(':')

# eb1 = plt.errorbar(x=columns, y=requirement_means_parallel_x3,
#                   yerr=[requirement_errors_parallel_x3, requirement_errors_parallel_x3],
#                   capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
# eb1[-1][0].set_linestyle(':')

eb2 = plt.errorbar(x=columns, y=requirement_means_serial_x2,
                  yerr=[requirement_errors_serial_x2, requirement_errors_serial_x2],
                  capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb2[-1][0].set_linestyle(':')

plt.plot(columns, len(columns) * [1.1e-4], linestyle='-', color='r')
plt.plot(columns, len(columns) * [-1.1e-4], linestyle='-', color='r')

plt.legend(handles=[eb0, eb2], labels=['Parallel x2', 'Serial x2'], fontsize=25)
plt.xlabel('Number of columns / rows', fontsize=12)
plt.ylabel(r'$\Delta e_{\rm 1}$', fontsize=12)

plt.savefig(plot_path + '/requirements.png')
plt.show()