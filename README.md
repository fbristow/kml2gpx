This is a little script to merge together location data from Google's Timeline with a GPX file that's exported from Strava.

This will take points from the KML file that have times that are later than the last point in the GPX file and append those points to the GPX file.

Output is on standard output.

Install and run with [Pipenv](https://docs.pipenv.org/).
