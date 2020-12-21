{pkgs ? import <nixpkgs> {}}:
with pkgs;
stdenv.mkDerivation {
    name = "apgte";
    buildInputs = [
        (python38.withPackages (p: [
            p.beautifulsoup4 
            (p.callPackage ebooklib/default.nix {})
        ]))
    ];
}
