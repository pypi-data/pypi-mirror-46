#!/bin/bash

# 204: Lines should be no longer than 160 chars
# 306: Shells that use pipes should set the pipefail option
# 602: Don't compare to empty string
# ANSIBLE0006: Using command rather than module
#   we have a few use cases where we need to use curl and rsync
# ANSIBLE0016: Tasks that run when changed should likely be handlers
#   this requires refactoring roles, skipping for now
SKIPLIST="ANSIBLE0006,ANSIBLE0016,204,306,602"

pushd validations
for playbook in `find . -type f -regex '.*\.y[a]?ml'`; do
    ansible-lint -vvv -x $SKIPLIST $playbook || lint_error=1
done
popd

# exit with 1 if we had a least an error or warning.
if [[ -n "$lint_error" ]]; then
    exit 1;
fi

