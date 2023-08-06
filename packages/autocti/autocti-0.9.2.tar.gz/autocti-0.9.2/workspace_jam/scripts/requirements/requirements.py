
import matplotlib.pyplot as plt

from workspace_jam.scripts.requirements import parallel_x2_requirements
from workspace_jam.scripts.requirements import parallel_x3_requirements
from workspace_jam.scripts.requirements import serial_x2_requirements

ci_resolutions = ['low_resolution', 'mid_resolution']  # , 'high_resolution']

# requirement_means_parallel_x2, requirement_errors_parallel_x2 = \
#     parallel_x2_requirements.parallel_x2_requirements_of_resolutions(ci_resolutions=ci_resolutions)

# requirement_means_parallel_x3, requirement_errors_parallel_x3 = \
 #    parallel_x3_requirements.parallel_x3_requirements_of_resolutions(ci_resolutions=ci_resolutions)

requirement_means_serial_x2, requirement_errors_serial_x2 = \
    serial_x2_requirements.serial_x2_requirements_of_resolutions(ci_resolutions=ci_resolutions)

columns = [517, 1034]#, 2068]#, 4136]

plt.figure(figsize=(20, 15))
plt.suptitle('Requirements for CTI Models', fontsize=20)

eb0 = plt.errorbar(x=columns, y=requirement_means_parallel_x2,
                  yerr=[requirement_errors_parallel_x2, requirement_errors_parallel_x2],
                  capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb0[-1][0].set_linestyle(':')

eb1 = plt.errorbar(x=columns, y=requirement_means_parallel_x3,
                  yerr=[requirement_errors_parallel_x3, requirement_errors_parallel_x3],
                  capsize=10, elinewidth=2, markeredgewidth=5, linestyle=':')
eb1[-1][0].set_linestyle(':')

plt.plot(columns, len(columns) * [1.0], linestyle='-', color='r')
plt.plot(columns, len(columns) * [-1.0], linestyle='-', color='r')

plt.legend(handles=[eb0, eb1], labels=['Parallel x2', 'Parallel x3'], fontsize=25)
plt.xlabel('Number of columns', fontsize=12)
plt.ylabel('Delta Ellipticity / Requirement (1.1e-4)', fontsize=12)
plt.show()