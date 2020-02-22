

with import <nixpkgs> { };

stdenv.mkDerivation {
    name = "default";
    
    buildInputs = [
		python37Packages.virtualenvwrapper
		python37Packages.pip
    ];
}
