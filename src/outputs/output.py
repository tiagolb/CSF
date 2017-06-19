#!/usr/bin/env python

import os
import glob
from html_assets import *
import urllib
import datetime
import HTML

AUDIT_DIR = "audit_result"

# convert timestamps to user friendly time strings
def time_convert(time_long):
    return datetime.datetime.fromtimestamp(
        int(time_long)
    ).strftime('%Y-%m-%d %H:%M:%S')

# decode url encoded strings
def urldecode(string):
    return urllib.unquote(string)

class Output():
    def __build_html_header(self):
        head = header.header_html(self.module, self.modules)
        return head

    def __build_index_header(self, newTitle):
        #Check which analysis results are already in the audit folder.
        #Reconstruct audit.html index accordingly
        imgAuditLoc = 'audit_result/' + self.fileHash
        auditFiles = os.listdir(imgAuditLoc)

        if("audit.html" in auditFiles):
            auditFiles.remove("audit.html")

        for n, module in enumerate(auditFiles):
            auditFiles[n] = os.path.splitext(module)[0]

        analysisHyperlinks = self.modules  + auditFiles
        head = header.header_html(newTitle, analysisHyperlinks)

        return head

    def __build_html_footer(self):
        foot = footer.footer_html()
        return foot

    def __build_index(self):
        header_code = self.__build_index_header("RAMAS")
        footer_code = self.__build_html_footer()
        html_code = """
            <div class="row">
              <div class="col-md-2"></div>
              <div class="col-md-8">
                <h1>RAMAS</h1>
                <h3 class="text-justify">This is RAMAS, a data-carving utility designed to extract data from conversations that took place while using applications such as Facebook, Twitter and more.</h3>
                <h3 class="text-justify">RAMAS was implemented for the Ciber Forensic Security course at Instituto Superior Tecnico and is available at this <a href="http://tiagolb.github.io/CSF/">GitHub page</a>.</h3>

                <h4 class="text-center">
                    <br/>
                    Project by:<br/>
                    Tiago Brito<br/>
                    Diogo Barradas<br/>
                    David Duarte
                </h4>
                </div>
              <div class="col-md-2"></div>
            </div>
        """
        file_handler = open(AUDIT_DIR + "/" + self.fileHash + "/audit.html" , "w")
        file_handler.write(header_code)
        file_handler.write(html_code)
        file_handler.write(footer_code)
        file_handler.close()

    def __create_directories(self):
        if not os.path.exists(AUDIT_DIR):
            os.makedirs(AUDIT_DIR)
        if not os.path.exists(AUDIT_DIR + "/" + self.fileHash):
            os.makedirs(AUDIT_DIR + "/" + self.fileHash)
        self.__build_index()

    def setup(self, fileHash, module, modules):
        self.fileHash = fileHash
        self.modules = modules
        self.module = module
        self.html_filename = "/" + fileHash + "/" + module + ".html"
        self.__create_directories()

    def html_code(self, input_list, fields):
        t = HTML.Table(
                header_row=fields,
                classes="table table-striped"
            )
        for message in input_list:
            t.rows.append(message)
        return str(t)

    def out(self, input_list, recordFields):

        #TODO Re-generate module audit header to account for newly analyzed modules
        # generate header and footer html code
        header_code = self.__build_html_header()
        footer_code = self.__build_html_footer()

        # create html file for this target
        file_handler = open(AUDIT_DIR + self.html_filename, "w")
        file_handler.write(header_code) # write header code
        file_handler.write("<h1>"+ self.module +"</h1>")
        file_handler.write(self.html_code(input_list, recordFields)) # write results
        file_handler.write(footer_code) # write footer code
        file_handler.close() # close file
