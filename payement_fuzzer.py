"""
find_hidden_payment_gateway

Copyright 2006 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import re
import itertools

import w3af.core.controllers.output_manager as om
import w3af.core.data.kb.config as cf
import w3af.core.data.parsers.parser_cache as parser_cache
import w3af.core.data.constants.response_codes as http_constants

from w3af.core.controllers.plugins.crawl_plugin import CrawlPlugin
from w3af.core.controllers.core_helpers.fingerprint_404 import is_404
from w3af.core.controllers.misc.itertools_toolset import unique_justseen
from w3af.core.controllers.exceptions import BaseFrameworkException

from w3af.core.data.parsers.utils.header_link_extract import headers_url_generator
from w3af.core.data.db.variant_db import VariantDB
from w3af.core.data.bloomfilter.scalable_bloom import ScalableBloomFilter
from w3af.core.data.db.disk_set import DiskSet
from w3af.core.data.dc.headers import Headers
from w3af.core.data.dc.factory import dc_from_form_params
from w3af.core.data.dc.generic.form import Form
from w3af.core.data.dc.cookie import Cookie
from w3af.core.data.options.opt_factory import opt_factory
from w3af.core.data.options.option_types import BOOL, REGEX
from w3af.core.data.options.option_list import OptionList
from w3af.core.data.request.fuzzable_request import FuzzableRequest

class find_hidden_payment_gateway(CrawlPlugin):
    """
    Generate a list of potential payment confirmation pages.
    :author: Pierre Coiffey (pierre.coiffey@gmail.com)
    """

    UNAUTH_FORBID = {http_constants.UNAUTHORIZED, http_constants.FORBIDDEN}

    def __init__(self):
        CrawlPlugin.__init__(self)

        # Internal variables
        self._compiled_ignore_re = None
        self._compiled_follow_re = None
        self._broken_links = DiskSet(table_prefix='hidden_payment_gateway')
        self._first_run = True
        self._target_urls = []
		self._target_domain = None
        #self._already_filled_form = ScalableBloomFilter()
        #self._variant_db = VariantDB()

        # User configured variables
        self._ignore_regex = ''
        self._follow_regex = '.*'
        self._only_forward = False
        self._compile_re()

     def _handle_first_run(self):
        if not self._first_run:
            return

        # I have to set some variables, in order to be able to code
        # the "only_forward" feature
        self._first_run = False
        self._target_urls = [i.uri2url() for i in cf.cf.get('targets')]

        # The following line triggered lots of bugs when the "stop" button
        # was pressed and the core did this: "cf.cf.save('targets', [])"
        #
        #self._target_domain = cf.cf.get('targets')[0].get_domain()
        #
        #    Changing it to something awful but bug-free.
		targets = cf.cf.get('targets')
        if not targets:
            return

        self._target_domain = targets[0].get_domain()

	def generate_list(self):

		dirs = [
			'/',
			'/inc/',
			'/include/',
			'/include/pay/',
			'/includes/',
			'/includes/pay/',
			'/lib/',
			'/libraries/',
			'/module/',
			'/module/pay/',
			'/modules/',
			'/modules/pay/',
			'/payment/',
			'/shop/',
			'/store/',
			'/svc/',
			'/servlet/',
			'/cgi/',
			'/cgi-bin/',
			'/cgibin/',
		]		

		files = [
			'pay',
			'payment',
			'success',
			'paymentsuccess',
			'paymentcomplete',
			'paymentsuccessful',
			'successful',
			'paid',
			'return',
			'valid',
			'validpay',
			'validate',
			'validatepayment',
			'validatepay',
			'validation',
			'complete',
			'completepay',
			'completepayment',
			'trxcomplete',
			'transactioncomplete',
			'final',
			'finished',
		]	

		exts = [
			'',
			'.php',
			'.asp',
			'.aspx',
			'.jsp',
			'.py',
			'.pl',
			'.rb',
			'.cgi',
			'.php3',
			'.php4',
			'.php5',
		]		
	for dir in dirs:
    	for file in files:
        	for ext in exts:
            	print "{}{}{}\n".format(el,el1,el2)
