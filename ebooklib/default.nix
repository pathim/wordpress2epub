{buildPythonPackage, fetchPypi, lxml, six}:
let
	name = "EbookLib";
	version = "0.17.1";
in
	buildPythonPackage {
		pname = name;
		version = version;
		src = fetchPypi {
			pname = name;
			version = version;
			sha256 = "1w972g0kmh9cdxf3kjr7v4k99wvv4lxv3rxkip39c08550nf48zy";
		};
		propagatedBuildInputs = [lxml six];
	}