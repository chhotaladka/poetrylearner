#!/bin/bash
#
# name: build_scripts.sh
# info: Combine all javascripts/css to create single javascripts/css file
#      and minimize it.
# Note: Do not change the path of this file, rules depend on relative path.
# =========================================================================

## Output javascript file
TARGET_JS="poetry/static/js/poetrylearner.js"
TARGET_JS_MIN="poetry/static/js/poetrylearner.min.js"


## Input javascript files
SHARED_JS="poetry/static/js/shared.js"
MODAL_JS="poetry/static/js/modal.js"
FEEDBACK_JS="feedback/static/feedback/js/feedback.js"
BOOKMARK_JS="bookmarks/static/bookmarks/js/bookmark.js"
REPOSITORY_JS="repository/static/repository/js/repository.js"
ACTIVITY_JS="activity/static/activity/js/activity.js"

INPUT_JS_FILES="${SHARED_JS} ${MODAL_JS} ${FEEDBACK_JS} ${BOOKMARK_JS} ${REPOSITORY_JS} ${ACTIVITY_JS}"


## Create Output javascript file and minimize it
echo "Creating targte javasctipt..."
cat ${INPUT_JS_FILES} > ${TARGET_JS}
echo "Created ${TARGET_JS}"
echo "Minimizing ${TARGET_JS}"
cp ${TARGET_JS} ${TARGET_JS_MIN}
echo "Created ${TARGET_JS_MIN}"

