#!/usr/bin/env perl

#
#
# This Script is used to generate LaTeX files from the .cxx source
# files in the Insight/Examples directory.
# 
# This automatic generation mechanism guarranties that the code 
# presented on the SoftwareGuide book matches exactly the code
# the is compiled and updated in the source repository.
#
# This script is expected to be invoked by CMake.
#
#

print "number of arguments =  $#ARGV \n";

if( $#ARGV < 1 )
  {
  print "Usage: ".$ARG0." <input file with list of inputs> <output path> \n";
  exit;
  }

open(INLISTFILE, "$ARGV[0]"  )  or die "Can't open $ARGV[0] $!";
my @inputfiles = <INLISTFILE>;


foreach (@inputfiles) {
  ParseCxxFile( $_ , $ARGV[1] );
}







#
#  Subroutine for parsing each one of the .cxx files.
#  A LaTeX file is produced as a result
#
sub ParseCxxFile {

  my $inputfilename  = shift;
  my $outputfilename = shift;

  my $basefilename = $inputfilename;

  $basefilename =~ s/.*\///;
  $basefilename =~ s/\.cxx/.tex/;
  
  $outputfilename .= "/".$basefilename;

  # truncate the initial part of the path
  $inputfilename =~ /(Examples\/.*$)/;
  my $examplefilename = $1;

  print "Processing $inputfilename into $outputfilename  ... \n";

  open(INFILE,    "$inputfilename"  )  or die "Can't open $inputfilename $!";
  open(OUTFILE,  ">$outputfilename" )  or die "Can't open $outputfilename $!";

  my $beginlatextag = "BeginLatex";
  my $endlatextag   = "EndLatex";

  my $begincodesnippettag = "BeginCodeSnippet";
  my $endcodesnippettag   = "EndCodeSnippet";

  my $dumpinglatex = 0;
  my $dumpingcode  = 0;



  # The following message is a warning writen on the generated .tex
  # files for preventing them from being manualy edited.
  print OUTFILE "\% Please do NOT edit this file.\n";
  print OUTFILE "\% It has been automatically generated\n";
  print OUTFILE "\% by a perl script from the original cxx sources\n";
  print OUTFILE "\% in the Insight/Examples directory\n\n";
  print OUTFILE "\% Any changes should be made in the file\n";
  print OUTFILE "\% $inputfilename\n";
  print OUTFILE "\n\n";



  # The following message will show up in the actual text preceding
  # any of the examples. That facilitate users to relate to code in 
  # the source tree.
  print OUTFILE "The source code of this section can be found in the file\\\\\n";
  print OUTFILE "\\texttt\{$examplefilename\}\n\n";



  while(<INFILE>) {

    my $tagfound     = 0;

    if( /$beginlatextag/ ) {
      $tagfound = 1;
      $dumpinglatex = 1;
      $dumpingcode  = 0;
      }
    elsif( /$begincodesnippettag/ ) {
      $tagfound = 1;
      $dumpinglatex = 0;
      $dumpingcode  = 1;
      print OUTFILE "\\small\n";
      print OUTFILE "\\begin{verbatim}\n";
      }
    elsif( /$endlatextag/ ) {
      $tagfound = 1;
      $dumpinglatex = 0;
      }
    elsif( /$endcodesnippettag/ ) {
      $tagfound = 1;
      $dumpingcode = 0;
      print OUTFILE "\\end{verbatim}\n";
      }
    if( !$tagfound ) {
      if( $dumpinglatex ) {
        my $outline = $_;
        $outline =~ s/\/\///; 
        print OUTFILE "$outline";
        }
      if( $dumpingcode ) {
        print OUTFILE "$_";
        }
      }

  }

}


