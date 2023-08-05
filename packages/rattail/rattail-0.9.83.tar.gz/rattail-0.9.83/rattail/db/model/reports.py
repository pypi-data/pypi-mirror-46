# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Data models for reporting
"""

from __future__ import unicode_literals, absolute_import

import sqlalchemy as sa

from rattail.db.model import Base, ExportMixin
from rattail.db.core import filename_column
from rattail.util import NOTSET


class ReportOutput(ExportMixin, Base):
    """
    Represents a generated report(s)
    """
    __tablename__ = 'report_output'
    model_title = "Generated Report"

    report_name = sa.Column(sa.String(length=255), nullable=True)
    filename = filename_column()

    def filepath(self, config, filename=NOTSET, **kwargs):
        if filename is NOTSET:
            filename = self.filename
        return super(ReportOutput, self).filepath(config, filename=filename, **kwargs)
