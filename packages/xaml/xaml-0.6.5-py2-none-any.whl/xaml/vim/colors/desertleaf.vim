" Vim color file
" Maintainer:   Ethan Furman <ethan@earths-treasure.com>
" Last Change:  01 Apr 2005

" cool help screens
" :he group-name
" :he highlight-groups
" :he cterm-colors

set background=dark
if version > 580
    " no guarantees for version 5.8 and below, but this makes it stop
    " complaining
    hi clear
    if exists("syntax_on")
    syntax reset
    endif
endif
let g:colors_name="desertleaf"

hi Normal   guifg=White guibg=grey20

" highlight groups
hi Cursor   guibg=khaki guifg=slategrey
"hi CursorIM
"hi Directory
"hi DiffAdd
"hi DiffChange
"hi DiffDelete
"hi DiffText
"hi ErrorMsg
hi VertSplit    guibg=#c2bfa5 guifg=grey50 gui=none
hi Folded   guibg=grey30 guifg=gold
hi FoldColumn   guibg=grey30 guifg=tan
hi IncSearch    guifg=slategrey guibg=khaki
"hi LineNr
hi ModeMsg  guifg=goldenrod
hi MoreMsg  guifg=SeaGreen
hi NonText  guifg=LightBlue guibg=grey60
hi Question guifg=springgreen
hi Search   guibg=LightBlue guifg=Black
hi SpecialKey   guifg=yellowgreen
hi StatusLine   guibg=#c2bfa5 guifg=black gui=none
hi StatusLineNC guibg=#c2bfa5 guifg=grey50 gui=none
hi Title    guifg=indianred
hi Visual   gui=none guifg=khaki guibg=olivedrab
"hi VisualNOS
hi WarningMsg   guifg=salmon
"hi WildMenu
"hi Menu
"hi Scrollbar
"hi Tooltip

" syntax highlighting groups
hi VarPrefix    guifg=orange ctermfg=white
hi Comment      guifg=SkyBlue ctermfg=blue
hi Constant     guifg=red ctermfg=red
hi Identifier   guifg=LightGreen  ctermfg=LightGreen
hi Number       guifg=cyan        ctermfg=cyan
hi PreProc      guifg=indianred ctermfg=LightRed
hi Statement    guifg=yellow  ctermfg=yellow
hi Special      guifg=navajowhite     guibg=black ctermfg=white
hi SpecialOne   guifg=cyan     guibg=black ctermfg=white
hi SpecialTwo   guifg=lightgreen     guibg=black ctermfg=white
hi SpecialThree guifg=orange     guibg=black ctermfg=white
hi SpecialFour  guifg=lightred     guibg=black ctermfg=white
hi SpecialFive  guifg=cornsilk3    guibg=black ctermfg=white
hi String       guifg=orange ctermfg=yellow
hi Type         guifg=darkkhaki   ctermfg=green
hi xamlQuote    guifg=orange guibg=black
"hi Underlined
hi Ignore     guifg=grey40
"hi Error
hi Todo     guifg=orangered guibg=yellow2

" color terminal definitions
hi SpecialKey   ctermfg=darkgreen
hi NonText      cterm=bold ctermfg=darkblue
hi Directory    ctermfg=darkcyan
hi ErrorMsg     cterm=bold ctermfg=7 ctermbg=1
hi IncSearch    cterm=NONE ctermfg=yellow ctermbg=green
hi Search       cterm=NONE ctermfg=grey ctermbg=blue
hi MoreMsg      ctermfg=darkgreen
hi ModeMsg      cterm=NONE ctermfg=brown
hi LineNr       ctermfg=3
hi Question     ctermfg=green
hi StatusLine   cterm=bold,reverse
hi StatusLineNC cterm=reverse
hi VertSplit    cterm=reverse
hi Title        ctermfg=5
hi Visual       cterm=reverse
hi VisualNOS    cterm=bold,underline
hi WarningMsg   ctermfg=1
hi WildMenu     ctermfg=0 ctermbg=3
hi Folded       ctermfg=darkgrey ctermbg=NONE
hi FoldColumn   ctermfg=darkgrey ctermbg=NONE
hi DiffAdd      ctermbg=4
hi DiffChange   ctermbg=5
hi DiffDelete   cterm=bold ctermfg=4 ctermbg=6
hi DiffText     cterm=bold ctermbg=1
hi Comment      ctermfg=darkcyan
hi Constant     ctermfg=brown
hi Special      ctermfg=5
hi Identifier   ctermfg=6
hi Statement    ctermfg=3
hi PreProc      ctermfg=5
hi Type         ctermfg=2
hi Underlined   cterm=underline ctermfg=5
hi Ignore       cterm=bold ctermfg=7
hi Ignore       ctermfg=darkgrey
hi Error        cterm=bold ctermfg=7 ctermbg=1


"vim: sw=4
