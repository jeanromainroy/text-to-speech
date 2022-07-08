#!/bin/bash

# clean current build files
cd public/build && rm bundle.* injection.*

# rebuild
npm run build
