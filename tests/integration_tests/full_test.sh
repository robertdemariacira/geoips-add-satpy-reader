# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # #
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # #
# # # This program is free software: you can redistribute it and/or modify it under
# # # the terms of the NRLMMD License included with this program. This program is
# # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
# # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
# # # for more details. If you did not receive the license, for more information see:
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

#!/bin/sh

$GEOIPS_PACKAGES_DIR/geoips/tests/integration_tests/full_install.sh exit_on_missing
if [[ "$?" != "0" ]]; then
    exit 1
fi
echo ""

# This should contain test calls to cover ALL required functionality tests for
# all available geoips plugin repositories on github.com

# The $GEOIPS_PACKAGES_DIR/geoips tests modules sourced within this script handle:
   # setting up the appropriate associative arrays for tracking the overall return value,
   # calling the test scripts appropriately, and
   # setting the final return value.

# Note you must use the variable "call" in the for the loop

# Argument to test_all_pre.sh ONLY sets the prefix on the log output / filenames.
# Used for clarity, and to differentiate potentially multiple "test_all.sh" scripts in the same repo.

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_pre.sh full

echo ""
# "call" used in test_all_run.sh
for call in \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/utils/check_code.sh all `dirname $0`/../ flake8_docstring_only" \
    "$GEOIPS_PACKAGES_DIR/geoips/docs/build_docs.sh `dirname $0`/../../ html_only" \
    "pytest $GEOIPS_PACKAGES_DIR/geoips/tests/test_pytest" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/abi.static.Infrared.imagery_annotated.sh" \
    "test_interfaces" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/abi.static.Visible.imagery_annotated.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/abi.config_based_output_low_memory.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/abi.config_based_output.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/ahi.tc.WV.geotiff.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/amsr2.tc.89H-Physical.imagery_annotated.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/amsr2_ocean.tc.windspeed.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/amsr2.config_based_no_compare.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/amsr2.config_based_overlay_output.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/amsr2.config_based_overlay_output_low_memory.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/ascat_knmi.tc.windbarbs.imagery_windbarbs_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/ascat_low_knmi.tc.windbarbs.imagery_windbarbs.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/ascat_uhr.tc.wind-ambiguities.imagery_windbarbs.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/gmi.tc.89pct.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/imerg.tc.Rain.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/oscat_knmi.tc.windbarbs.imagery_windbarbs.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/sar.tc.nrcs.imagery_annotated.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/smap.unsectored.text_winds.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/viirsday.tc.Night-Vis-IR.imagery_annotated.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/viirsmoon.tc.Night-Vis-GeoIPS1.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips/tests/scripts/viirsclearnight.Night-Vis-IR-GeoIPS1.unprojected_image.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/abi.tc.Visible.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/amsr2.tc.color37.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/amsr2.tc.windspeed.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/ascat_uhr.tc.nrcs.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/ascat_uhr.tc.windbarbs.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/imerg.tc.Rain.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/metopc_knmi_125.tc.windbarbs.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/oscat.tc.windspeed.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/sar.tc.nrcs.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/smap.tc.windspeed.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/recenter_tc/tests/scripts/viirs.tc.Infrared-Gray.imagery_clean.sh" \
    "$GEOIPS_PACKAGES_DIR/template_basic_plugin/tests/test_all.sh" \
    "$GEOIPS_PACKAGES_DIR/template_fusion_plugin/tests/test_all.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_plugin_example/tests/test_all.sh" \
    "$GEOIPS_PACKAGES_DIR/geoips_clavrx/tests/test_all.sh" \
    "$GEOIPS_PACKAGES_DIR/data_fusion/tests/test_all.sh"
do
    . $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_run.sh
done

. $GEOIPS_PACKAGES_DIR/geoips/tests/utils/test_all_post.sh