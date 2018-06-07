#!/bin/bash
cd ..
./gradlew --parallel -xtransformClassesAndResourcesWithProguardForRelease build
