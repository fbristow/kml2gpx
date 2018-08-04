#!/usr/bin/python3

from fastkml import kml
from pygeoif import geometry
import gpxpy
import sys, time, datetime, argparse

parser = argparse.ArgumentParser(description="merge KML with GPX")
parser.add_argument('--kml', type=str, dest='kml', help='the KML file', required=True)
parser.add_argument('--gpx', type=str, dest='gpx', help='the GPX file', required=True)
args = parser.parse_args()

with open(args.kml) as myfile:
    doc = myfile.read()

k = kml.KML()
k.from_string(doc)

# assume that there's 1 item in the document
(doc,) = k.features()
points = []

for feat in doc.features():
    if len(feat.geometry.coords) > 1 and feat.name != 'Driving':
        start = feat.begin.timestamp()
        end = feat.end.timestamp()
        step = (end - start) / len(feat.geometry.geoms)
        for point in feat.geometry.geoms:
            points.append((point, datetime.datetime.utcfromtimestamp(start)))
            start += step

with open(args.gpx) as myfile:
    doc = myfile.read()

gpx = gpxpy.parse(doc)

times = []
segment_points = gpx.tracks[0].segments[0].points
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            p = geometry.Point(point.longitude, point.latitude)
            times.append((p, point.time))

max_time = times[-1][1]
for point in points:
    if point[1] > max_time:
        p = point[0]
        segment_points.append(gpxpy.gpx.GPXTrackPoint(longitude=p.x, latitude=p.y, time=point[1], comment='source is KML'))

print(gpx.to_xml())
