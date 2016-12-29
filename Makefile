RSYNC=rsync -zcav \
	--exclude=\*~ --exclude=.\* \
	--delete-excluded --delete-after \
	--no-owner --no-group \
	--progress --stats


doc: .sphinx-stamp

upload-doc:
	$(RSYNC) build/doc/ dcmod.org:~/public_html/geotiler

.sphinx-stamp: .map-stamp
	sphinx-build doc build/doc

.map-stamp:
	./bin/geotiler-lint --cache redis -c -6.069 53.390 -s 512 512 -z 15 doc/map-osm.png
	./bin/geotiler-lint --cache redis -c -6.069 53.390 -s 512 512 -z 15 -p stamen-toner doc/map-stamen-toner.png
	./bin/geotiler-lint --cache redis -c -6.069 53.390 -z 8 -s 512 512 -p bluemarble doc/map-bluemarble.png
	./bin/geotiler-route -r 5 -a 1 --cache redis data/path.gpx doc/map-path.png
