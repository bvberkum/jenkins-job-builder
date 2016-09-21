# Copyright 2015 BrixCRM B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
The `pipeline` module supports the dsl attribute for The Pipeline (formerly Workflow)
projects, either using verbatim pipeline DSL script, or by (multi-)SCM.

**Component**: dsl
  :Macro: dsl
  :Entry Point: jenkins_jobs.pipeline


A pipeline job processes a script, that is given verbatim in the job config or
loaded from a file named 'Jenkinsfile' by default.
Alternatively, the job embeds a MultiSCM to get the script file.

::

    - job:
        project-type: workflow
        sandbox: false
        dsl:
            script: |
                job "my-job"

::

    - job:
        project-type: workflow
        sandbox: false
        dsl:
            scm:
            - git:
                branch:
                - origin/master
            script-file: Jenkinsfile


Job example:

    .. literalinclude::
      /../../tests/yamlparser/fixtures/project_workflow_template001.yaml

Job template example:

    .. literalinclude::
      /../../tests/yamlparser/fixtures/project_workflow_template002.yaml

"""

import logging
import xml.etree.ElementTree as XML

from jenkins_jobs.errors import InvalidAttributeError
from jenkins_jobs.errors import JenkinsJobsException
from jenkins_jobs.errors import MissingAttributeError
import jenkins_jobs.modules.base
from jenkins_jobs.modules.helpers import convert_mapping_to_xml

logger = logging.getLogger(str(__name__))



class DSL(jenkins_jobs.modules.base.Base):
    sequence = 35

    component_type = 'dsl'
    component_list_type = 'dsl'

    def gen_xml(self, xml_parent, data):

        if not 'dsl' in data:
            return

        dsl = data['dsl']

        if 'script' in dsl:
            class_ = 'org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition'

        elif 'scm' in dsl:
            class_ = 'org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition'
        else:
            raise MissingAttributeError('script or scm')

        xml_definition = XML.SubElement(xml_parent, 'definition',
                                        {'plugin': 'workflow-cps',
                                         'class': class_})

        needs_workspace = data.get('sandbox', False)
        XML.SubElement(xml_definition, 'sandbox').text = str(
            needs_workspace).lower()

        if 'script' in dsl:
            XML.SubElement(xml_definition, 'script').text = dsl['script']

        elif 'scm' in dsl:

            script_file = dsl.get('script-name', 'Jenkinsfile')
            XML.SubElement(xml_definition, 'scriptPath').text = str(script_file)

            scms_parent = XML.Element('scms')
            for scm in dsl.get('scm', []):
                self.registry.dispatch('scm', scms_parent, scm)
            scms_count = len(scms_parent)
            if scms_count == 0:
                XML.SubElement(xml_definition, 'scm', {'class': 'hudson.scm.NullSCM'})
            elif scms_count == 1:
                xml_definition.append(scms_parent[0])
            else:
                class_name = 'org.jenkinsci.plugins.multiplescms.MultiSCM'
                xml_attribs = {'class': class_name}
                xml_scm = XML.SubElement(xml_definition, 'scm', xml_attribs)
                xml_scm.append(scms_parent)



