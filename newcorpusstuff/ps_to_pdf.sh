#! /bin/bash
#
#  ps_to_pdf.sh
#
#  Description:
#
#    This bash script will use the "convert" program, and for each
#    file in the current directory with a ".ps" extension, will
#    create a converted copy with ".pdf" extension.
#
#  Modified:
#
#    31 March 2016
#
#  Author:
#
#    John Burkardt
#
let "n = 0"
pdf=".pdf"

for PSFILE in `ls -1 *.ps`;

  do
#
#  Get the "first name" of the file.
#
    firstname="${PSFILE%%.*}"
#
#  PDFFILE = firstname + "pdf"
#
    PDFFILE="$firstname$pdf"
#
#  Call CONVERT.
#
    convert $PSFILE $PDFFILE 
#
#  Report the current action.
#
    echo "Convert $PSFILE to $PDFFILE"
#
#  Report any failure.
#
    if [ $? -ne 0 ]; then
      echo "Could not convert " $PSFILE
    else
      let "n = n + 1"
    fi

  done
#
echo "Converted $n files."
