#!/usr/bin/env bash

_aiscalator_completion() {
    local IFS=$'
'
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _AISCALATOR_COMPLETE=complete $1 ) )
    return 0
}

_aiscalator_completionetup() {
    local COMPLETION_OPTIONS=""
    local BASH_VERSION_ARR=(${BASH_VERSION//./ })
    # Only BASH version 4.4 and later have the nosort option.
    if [ ${BASH_VERSION_ARR[0]} -gt 4 ] || ([ ${BASH_VERSION_ARR[0]} -eq 4 ] && [ ${BASH_VERSION_ARR[1]} -ge 4 ]); then
        COMPLETION_OPTIONS="-o nosort"
    fi

    complete $COMPLETION_OPTIONS -F _aiscalator_completion aiscalator
}

_aiscalator_completionetup;
