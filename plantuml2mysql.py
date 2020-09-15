#!/usr/bin/env python3
#-*-coding:utf-8-*-
# Usage: ./plantuml2mysql <dbsource.plu> <dbname>
# Author: Alexander I.Grafov <grafov@gmail.com>
# See https://github.com/grafov/plantuml2mysql
# The code is public domain.

CHARSET="utf8_unicode_ci"

import sys
import re
import time

# PlantUML allows some HTML tags in comments.
# We don't want them anymore here...
TAG_RE = re.compile(r'<[^>]+>')
def strip_html_tags(t):
    return TAG_RE.sub('', t)

# A minimal help
def print_usage():
  print("Convert PlantUML classes schema into mySQL database creation script")
  print("Usage:\n", sys.argv[0], "<dbsource.plu> <dbname>")
  print("\nSee https://github.com/grafov/plantuml2mysql for details\n")

def main():
    # Check arguments (exactly 1 + 2):
    if len(sys.argv) != 4:
        print_usage()
        sys.exit()
    try: # Avoid exception on STDOUT
        with open(sys.argv[1], 'r', encoding='UTF-8') as src:
            data = src.readlines()
    except:
        print("Cannot open file: '" + sys.argv[1] + "'")
        sys.exit()
    try: #
        with open(sys.argv[3],'w+', encoding='UTF-8') as dest:
            # Add information for future self ;-)
            dest.writelines(["# Database created on", time.strftime('%d/%m/%y %H:%M',time.localtime()), "from", sys.argv[1],"\n"])
            dest.writelines(["CREATE DATABASE %s CHARACTER SET = utf8mb4 COLLATE = %s;\n" % (sys.argv[2], CHARSET)])
            dest.writelines(["USE %s;\n" % sys.argv[2]])
            #print("# Database created on", time.strftime('%d/%m/%y %H:%M',time.localtime()), "from", sys.argv[1])
            #print("CREATE DATABASE %s CHARACTER SET = utf8mb4 COLLATE = %s;" % (sys.argv[2], CHARSET))
            #print("USE %s;\n" % sys.argv[2])
            uml = False; table = False; field = False
            primary = []; index = ""
            for l in data:
                l = l.strip()
                if not l:
                    continue
                if l == "```plantuml":
                    uml = True
                    continue
                if not uml:
                    continue
                if l == "```":
                    uml = False
                    continue
                if "--" in l: # only one --
                    dest.writelines(l.strip()+"\n")
                    continue
                temp = l.split('\'')
                length = len(temp)
                fieldDetail = ""
                if length > 3: # default value is varchar
                    fieldDetail = "\'".join(temp[0:length-2])
                    comment = temp[length-2]
                else:
                    fieldDetail = temp[0]
                i = fieldDetail.split()
                fname = i[0]
                if fname == ".." or fname == "__": # Separators in table definition
                    continue
                pk = False; idx = False
                if fname[0] in ("+", "#"):
                    if fname[0] == "#":
                        pk = True
                    else:
                        idx = True
                    fname = fname[1:]
                columnComment = ""
                if field and len(temp)>1 and len(temp)<=3:
                    columnComment = temp[1]
                if field and len(temp)>3:
                    columnComment = comment
                if l.startswith("entity"):
                    table = True; field = False
                    primary = []; index = ""
                    # Table names are quoted and lower cased to avoid conflict with a mySQL reserved wordpr
                    dest.writelines(["\ndrop table if exists `" +i[1].lower() + "`;\n"])
                    #print("drop table if exists `" +i[1].lower() + "`;")
                    dest.writelines(["CREATE TABLE `" + i[1].lower() + "` (\n"])
                    #print("CREATE TABLE `" + i[1].lower() + "` (")
                    continue
                if table and not field:
                    if l == "==": # Seperator after table description
                        field = True
                        continue
                    else:
                        tableComment = l
                if field and l == "}":
                    table = False; field = False
                    dest.writelines(["  creator          VARCHAR(64)  NULL,\n"])
                    #print(" creator          VARCHAR(64)  NULL,")
                    dest.writelines(["  gmt_create       DATETIME     NULL,\n"])
                    #print(" gmt_create       DATETIME     NULL,")
                    dest.writelines(["  updater          VARCHAR(64)  NULL,\n"])
                    #print(" updater          VARCHAR(64)  NULL,")
                    dest.writelines(["  gmt_modified     DATETIME     NULL,\n"])
                    #print(" gmt_modified     DATETIME     NULL,")
                    dest.writelines([" PRIMARY KEY (%s)" % ", ".join(primary)])
                    #print(" PRIMARY KEY (%s)" % ", ".join(primary), end="")
                    if index:
                        dest.write(",\n%s\n" % index[:-2],)
                        #print(",\n%s" % index[:-2],)
                        index = ""
                    dest.write(") COMMENT \'%s\';\n" % tableComment.strip())
                    #print(") COMMENT \'%s\';\n" % tableComment.strip())
                    continue
                if field and l == "#id":
                    dest.write("  %-16s SERIAL," % "id\n")
                    #print("  %-16s SERIAL," % "id")
                if field and l != "#id":
                    dest.writelines("  %-16s %s " % (fname, " ".join(i[1:]).upper()))
                    #print("  %-16s %s" % (fname, " ".join(i[1:]).upper()), end=" ")
                    if columnComment: #other description
                        # Avoid conflict with apostrophes (use double quotation marks)
                        dest.writelines(" COMMENT %s" % strip_html_tags(columnComment.strip()))
                        #print(" COMMENT \'%s\'" % strip_html_tags(columnComment.strip()), end="")
                    dest.write(",\n")
                    #print(",")
                if field and pk:
                    primary.append(fname)
                if field and idx:
                    index += "  INDEX (%s),\n" % fname
    except:
        print("Cannot open file: '" + sys.argv[3] + "'")
        sys.exit()

if __name__ == "__main__":
    main()
