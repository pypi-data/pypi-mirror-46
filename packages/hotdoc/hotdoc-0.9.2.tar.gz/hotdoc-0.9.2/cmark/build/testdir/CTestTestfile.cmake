# CMake generated Testfile for 
# Source directory: /home/meh/devel/hotdoc/cmark/test
# Build directory: /home/meh/devel/hotdoc/cmark/build/testdir
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(api_test "/home/meh/devel/hotdoc/cmark/build/api_test/api_test")
add_test(html_normalization "/usr/bin/python3" "-m" "doctest" "/home/meh/devel/hotdoc/cmark/test/normalize.py")
add_test(spectest_library "/usr/bin/python3" "/home/meh/devel/hotdoc/cmark/test/spec_tests.py" "--no-normalize" "--spec" "/home/meh/devel/hotdoc/cmark/test/spec.txt" "--library-dir" "/home/meh/devel/hotdoc/cmark/build/testdir/../src")
add_test(pathological_tests_library "/usr/bin/python3" "/home/meh/devel/hotdoc/cmark/test/pathological_tests.py" "--library-dir" "/home/meh/devel/hotdoc/cmark/build/testdir/../src")
add_test(roundtriptest_library "/usr/bin/python3" "/home/meh/devel/hotdoc/cmark/test/roundtrip_tests.py" "--spec" "/home/meh/devel/hotdoc/cmark/test/spec.txt" "--library-dir" "/home/meh/devel/hotdoc/cmark/build/testdir/../src")
add_test(entity_library "/usr/bin/python3" "/home/meh/devel/hotdoc/cmark/test/entity_tests.py" "--library-dir" "/home/meh/devel/hotdoc/cmark/build/testdir/../src")
add_test(spectest_executable "/usr/bin/python3" "/home/meh/devel/hotdoc/cmark/test/spec_tests.py" "--no-normalize" "--spec" "/home/meh/devel/hotdoc/cmark/test/spec.txt" "--program" "/home/meh/devel/hotdoc/cmark/build/testdir/../src/cmark")
add_test(smartpuncttest_executable "/usr/bin/python3" "/home/meh/devel/hotdoc/cmark/test/spec_tests.py" "--no-normalize" "--spec" "/home/meh/devel/hotdoc/cmark/test/smart_punct.txt" "--program" "/home/meh/devel/hotdoc/cmark/build/testdir/../src/cmark --smart")
add_test(regressiontest_executable "/usr/bin/python3" "/home/meh/devel/hotdoc/cmark/test/spec_tests.py" "--no-normalize" "--spec" "/home/meh/devel/hotdoc/cmark/test/regression.txt" "--program" "/home/meh/devel/hotdoc/cmark/build/testdir/../src/cmark")
