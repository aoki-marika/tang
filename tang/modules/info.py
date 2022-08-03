class InfoModule:
    """
    The "info" module for a controller, responsible for providing metadata about
    the environment and program.
    """

    def __init__(self):
        self.requires_encryption = False

    def avs(self):
        """
        Get information about the Arcade Virtual System (AVS) module.
        """

        return [
            {
                'model': 'TNG',
                'ext': '202208031200',
                'dest': 'A',
                'spec': 'A',
                'rev': 'A',
                'services': 'http://tang.services/',
            },
        ]

    def launcher(self):
        """
        Get information about Spice.
        """

        return [
            {
                'version': '1.0',
                'compile_date': 'Aug 3 2022',
                'compile_time': '12:00:00',
                'system_time': '2022-08-03T12:00:00Z',
                'args': ['--arg1', '--arg2', '--arg3'],
            },
        ]

    def memory(self):
        """
        Get information about the system memory.
        """

#        info.AddMember("mem_total", memutils::mem_total(), alloc);
#        info.AddMember("mem_total_used", memutils::mem_total_used(), alloc);
#        info.AddMember("mem_used", memutils::mem_used(), alloc);
#        info.AddMember("vmem_total", memutils::vmem_total(), alloc);
#        info.AddMember("vmem_total_used", memutils::vmem_total_used(), alloc);
#        info.AddMember("vmem_used", memutils::vmem_used(), alloc);

        return [
            {
                "mem_total": 8 * 1000 * 1000,
                "mem_total_used": 4 * 1000 * 1000,
                "mem_used": 4 * 1000 * 1000,

                "vmem_total": 4 * 1000 * 1000,
                "vmem_total_used": 1 * 1000 * 1000,
                "vmem_used": 1 * 1000 * 1000,
            },
        ]
