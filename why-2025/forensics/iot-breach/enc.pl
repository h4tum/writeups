use strict;
use warnings;
use Crypt::Mode::CBC;
use File::Find;

# Check if password is provided
die "Usage: $0 <password>
" unless @ARGV == 1;
my $password = $ARGV[0];

# Define encryption parameters
my $cipher = Crypt::Mode::CBC->new("AES");

# Get all files in the current directory
find(sub {
    return if -d $_;  # Skip directories
    return if $_ =~ /.pl$/;
    encrypt_file($_);
}, ".");

sub encrypt_file {
    my ($file) = @_;

    # Read file contents
    open my $fh, '<', $file or die "Could not open '$file' for reading: $!";
    binmode $fh;
    my $data = do { local $/; <$fh> };
    close $fh;

    # Encrypt the data
    my $encrypted = $cipher->encrypt($data, $password, "R4ND0MivR4ND0Miv");

    # Write encrypted data back to file
    open my $fh_out, '>', "$file.enc" or die "Could not open '$file.enc' for writing: $!";
    binmode $fh_out;
    print $fh_out $encrypted;
    close $fh_out;

    print "Encrypted $file -> $file.enc
";
}

print "Encryption complete.
";