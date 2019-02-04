# -*- coding: utf-8 -*-
# Copyright (c) 2018 Christiaan Frans Rademan, David Kruger.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
from uuid import uuid4

from luxon import register
from luxon import SQLModel
from luxon.utils.timezone import now

# from infinitystone.models.elements import infinitystone_element
# from infinitystone.models.elements import infinitystone_element_tag

@register.model()
class netrino_service_template(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    name = SQLModel.String(null=False)
    creation_time = SQLModel.DateTime(default=now, readonly=True)
    primary_key = id
    unique_service_template = SQLModel.UniqueIndex(name)

@register.model()
class netrino_service_template_entry(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    service_template = SQLModel.Uuid()
    entry_no = SQLModel.Integer(null=False)
    yang_model = SQLModel.String(null=False)
    interface = SQLModel.Text(default="netconf")
    function = SQLModel.Text(default="config")
    method = SQLModel.Text()
    element = SQLModel.Uuid(null=True)
    element_tag = SQLModel.String(null=True)
    creation_time = SQLModel.DateTime(default=now, readonly=True)
    service_template_ref = SQLModel.ForeignKey(service_template,
                                               netrino_service_template.id)
    # element_ref = SQLModel.ForeignKey(element, infinitystone_element.id)
    # element_tag_ref = SQLModel.ForeignKey(element_tag,infinitystone_element_tag.name)
    unique_entry = SQLModel.UniqueIndex(service_template, entry_no)
    primary_key = id

@register.model()
class netrino_servicetemplate_pool(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    path = SQLModel.String(null=False)
    type = SQLModel.String(null=False)
    pool = SQLModel.String(null=False)
    servicetemplate_entry = SQLModel.Uuid(null=False)
    ste_pool_ref = SQLModel.ForeignKey(servicetemplate_entry,
                                             netrino_service_template_entry.id)
    servicetemplate_entry_index = SQLModel.Index(servicetemplate_entry)
    primary_key = id

@register.model()
class netrino_servicetemplate_mappings(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    path = SQLModel.String(null=False)
    mapper = SQLModel.String(null=False)
    mapper_data = SQLModel.Json()
    servicetemplate_entry = SQLModel.Uuid(null=False)
    ste_map_ref = SQLModel.ForeignKey(servicetemplate_entry,
                                             netrino_service_template_entry.id)
    servicetemplate_entry_index = SQLModel.Index(servicetemplate_entry)
    primary_key = id

@register.model()
class netrino_user_select(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    path = SQLModel.String(null=False)
    name = SQLModel.String()
    description = SQLModel.String()
    type = SQLModel.String(default='text')
    url = SQLModel.String()
    endpoint = SQLModel.String()
    servicetemplate_entry = SQLModel.Uuid(null=False)
    ste_userselect_ref = SQLModel.ForeignKey(servicetemplate_entry,
                                             netrino_service_template_entry.id)
    servicetemplate_entry_index = SQLModel.Index(servicetemplate_entry)
    primary_key = id

@register.model()
class netrino_task_output(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    path = SQLModel.String(null=False)
    entry_no = SQLModel.Integer(null=False)
    output_path = SQLModel.String(null=False)
    servicetemplate_entry = SQLModel.Uuid(null=False)
    ste_task_ref = SQLModel.ForeignKey(servicetemplate_entry,
                                             netrino_service_template_entry.id)
    servicetemplate_entry_index = SQLModel.Index(servicetemplate_entry)
    primary_key = id

@register.model()
class netrino_servicetemplate_static(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    path = SQLModel.String(null=False)
    value = SQLModel.String(null=False)
    type = SQLModel.String(default="str")
    servicetemplate_entry = SQLModel.Uuid(null=False)
    ste_static_ref = SQLModel.ForeignKey(servicetemplate_entry,
                                             netrino_service_template_entry.id)
    servicetemplate_entry_index = SQLModel.Index(servicetemplate_entry)
    primary_key = id

@register.model()
class netrino_servicetemplate_copy(SQLModel):
    """Used when a copy of an already entered/generated value is to be used.

    When entry_no is ommitted, THIS entry is assumed.
    """
    id = SQLModel.Uuid(default=uuid4, internal=True)
    path = SQLModel.String(null=False)
    source_path = SQLModel.String(null=False)
    entry_no = SQLModel.Integer()
    servicetemplate_entry = SQLModel.Uuid(null=False)
    ste_copy_ref = SQLModel.ForeignKey(servicetemplate_entry,
                                             netrino_service_template_entry.id)
    servicetemplate_entry_index = SQLModel.Index(servicetemplate_entry)
    primary_key = id