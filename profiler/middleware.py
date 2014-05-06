__author__ = 'vaibhav'

import cProfile
import os
import pstats
import tempfile
from cStringIO import StringIO
from django.conf import settings
from django.template.loader import render_to_string


class ProfileMiddleware(object):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            (fd, self.profiler_file) = tempfile.mkstemp()
            self.profiler.dump_stats(self.profiler_file)
            out = StringIO()
            stats = pstats.Stats(self.profiler_file, stream=out)
            stats.strip_dirs()          # Must happen prior to sort_stats
            if request.GET['prof']:
                stats.sort_stats(request.GET['prof'])
            stats.print_stats()
            os.unlink(self.profiler_file)
            profile_output = out.getvalue().split('\n')
            info = '\n'.join(profile_output[:6])
            table_header = [_ for _ in profile_output[6].split(' ') if _]
            table_rows = [_.split() for _ in profile_output[7:-3] if _]
            table_rows = [_[:5] + [' '.join(_[5:])] for _ in table_rows]
            ret_dict = dict(table_header=table_header,
                            table_rows=table_rows,
                            info=info)

            response.content = render_to_string('profiler.html', ret_dict)
        return response