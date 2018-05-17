#!/bin/bash
cd ..
./gradlew --parallel -xtransformClassesAndResourcesWithProguardForRelease assemble
