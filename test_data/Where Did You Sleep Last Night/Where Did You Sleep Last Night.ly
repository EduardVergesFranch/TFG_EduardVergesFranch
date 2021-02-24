\version "2.20.0"

%{ macro eps(scale, first_bar, last_bar, w) -%}
_\markup {
  \general-align #Y #DOWN {
    \epsfile #X #%{{scale}%} #"%{{ eps_waveform(first_bar, last_bar, w=w*5, h=0.5, right_border_shift=0) }%}"
  }
}
%{- endmacro %}
%{ macro color() -%}
     \override NoteHead.color = #(rgb-color%{{next_color()}%})
%{- endmacro %}

\pointAndClickOff

\header {
    tagline =  ""
    }

#(set-global-staff-size 20.00)
\paper {
    page-breaking = #ly:one-page-breaking

    paper-width = 22.86\cm
    paper-height = 30.47\cm
    top-margin = 1.49\cm
    bottom-margin = 1.49\cm
    left-margin = 1.49\cm
    right-margin = 1.49\cm
    between-system-space = 1.61\cm
    ragged-right = ##t
 }
\layout {
    indent=#0
    short-indent = #0
    \context { \Score
        proportionalNotationDuration = #(ly:make-moment 1/10)
        \override SpacingSpanner.strict-note-spacing = ##t
        \override SpacingSpanner.uniform-stretching = ##t
        \override NonMusicalPaperColumn.page-break-permission = ##f
        \override NonMusicalPaperColumn.line-break-permission = ##f
        skipBars = ##t
        autoBeaming = ##f
    }
}
PartPOneVoiceOne =  \relative a {
    \clef "treble" \time 3/4 \key c \major \transposition c \break
    | % 1
    \tempo 4=100 \stemUp %{{color()}%}  a2 %{{ eps(110,0, 7,2)}%} -\mp
    ^\markup{ \bold\small {\box "Intro" } } \stemUp %{{color()}%}  a4 | % 2
    \stemUp %{{color()}%}  e'2 \stemUp %{{color()}%}  e4 | % 3
    \stemUp %{{color()}%}  d2 \stemUp %{{color()}%}  e4 | % 4
    \stemUp %{{color()}%}  c2 \stemUp %{{color()}%}  d4 | % 5
    \stemUp %{{color()}%}  e2 \stemUp %{{color()}%}  d4 | % 6
    \stemUp %{{color()}%}  c2 \stemUp %{{color()}%}  b4 | % 7
    \stemUp %{{color()}%}  a2. | % 8
    R2. \bar ".|:-||" \break

    | % 9
    \stemUp %{{color()}%} <a e'>2 %{{ eps(110,8, 11,2)}%} ^\markup{
        \bold\small {\box "Verse" } } \stemUp %{{color()}%} <a e'>4 | \barNumberCheck #10
    \stemUp %{{color()}%} <a e'>2. | % 11
    \stemDown %{{color()}%} <d a' d fis>2. | % 12
    \stemUp %{{color()}%} <c e g c e>2. \break | % 13
    \stemUp %{{color()}%} <e, b' e gis b e>2. ~ ~ ~ ~ ~ ~ %{{eps(110,12, 15,2)}%} | % 14
    \stemUp <e b' e gis b e>2. | % 15
    \stemUp %{{color()}%} <a e'>2 \stemUp %{{color()}%} <a e'>4 | % 16
    \stemUp %{{color()}%} <a e'>2. \break

    |%17
    \stemUp %{{color()}%} <a e'>2 %{{ eps(110,16, 19,2)}%}
    \stemUp %{{color()}%} <a e'>4 | \barNumberCheck #18
    \stemUp %{{color()}%} <a e'>2. | % 19
    \stemDown %{{color()}%} <d a' d fis>2. | % 20
    \stemUp %{{color()}%} <c e g c e>2. \break | % 21
    \stemUp %{{color()}%} <e, b' e gis b e>2. ~ ~ ~ ~ ~ ~ %{{ eps(110,20, 23,2)}%} | % 22
    \stemUp <e b' e gis b e>2. | % 23
    \stemUp %{{color()}%} <a e'>2 \stemUp %{{color()}%} <a e'>4 | % 24
    \stemUp %{{color()}%} <a e'>2. \break


    | % 25
    \stemUp %{{color()}%}  a'2 %{{ eps(110,24, 31,2)}%} ^\markup{\bold\small {\box "Interlude" } }
    \stemUp %{{color()}%}  a4 | % 26
    \stemDown %{{color()}%}  e'2 \stemDown %{{color()}%}  e4 | % 27
    \stemDown %{{color()}%}  d2 \stemDown %{{color()}%}  e4 | \barNumberCheck #28
    \stemDown %{{color()}%}  c2 \stemDown %{{color()}%}  d4 | % 29
    \stemDown %{{color()}%}  e2 \stemDown %{{color()}%}  d4 | % 30
    \stemDown %{{color()}%}  c2 \stemDown %{{color()}%}  b4 | % 31
    \stemUp %{{color()}%}  a2. | % 32
    R2. \break

    | % 33
    \stemUp %{{color()}%} <a, e' a c e>4 %{{ eps(110,32, 35,2)}%} -\mf ^\markup{ \bold\small {\box "Verse" } }
    \stemUp %{{color()}%} <a e' a c e>4
    \stemUp %{{color()}%} <a e' a c e>4  | % 34
    \stemUp %{{color()}%} <a e' a c e>2. | % 35
    \stemDown %{{color()}%} <d a' d fis>2. | % 36
    \stemUp %{{color()}%} <c e g c e>2. \break | % 37
    \stemUp %{{color()}%} <e, b' e gis b e>2 %{{ eps(110,36,39,2)}%}
    \stemUp %{{color()}%} <e b' e gis b e>4 | \barNumberCheck #38
    \stemUp %{{color()}%} <e b' e gis b e>2. | % 39
    \stemUp %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4
    \stemUp %{{color()}%} <a e' a c e>4 | % 40
    \stemUp %{{color()}%} <a e' a c e>2. \break

    | % 41
    \stemUp %{{color()}%} <a, e' a c e>4 %{{ eps(110,40,43,2)}%} -\mf ^\markup{ \bold\small {\box "Verse" } }
    \stemUp %{{color()}%} <a e' a c e>4
    \stemUp %{{color()}%} <a e' a c e>4  | % 42
    \stemUp %{{color()}%} <a e' a c e>2. | % 43
    \stemDown %{{color()}%} <d a' d fis>2. | % 44
    \stemUp %{{color()}%} <c e g c e>2. \break | % 45
    \stemUp %{{color()}%} <e, b' e gis b e>2 %{{ eps(110,44,47,2)}%}
    \stemUp %{{color()}%} <e b' e gis b e>4 | \barNumberCheck #46
    \stemUp %{{color()}%} <e b' e gis b e>2. | % 47
    \stemUp %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4
    \stemUp %{{color()}%} <a e' a c e>4 | % 48
    \stemUp %{{color()}%} <a e' a c e>2. \break

    | % 49
    \stemUp %{{color()}%}  a2 %{{ eps(110,48, 55,2)}%} -\mp ^\markup{\bold\small {\box "Outro" } }
    \stemUp %{{color()}%}  a4 | % 50
    \stemUp %{{color()}%}  e'2 \stemUp %{{color()}%}  e4 | % 51
    \stemUp %{{color()}%}  d2 \stemUp %{{color()}%}  e4 | % 52
    \stemUp %{{color()}%}  c2 \stemUp %{{color()}%}  d4 | % 53
    \stemUp %{{color()}%}  e2 \stemUp %{{color()}%}  d4 | % 54
    \stemUp %{{color()}%}  c2 \stemUp %{{color()}%}  b4 | % 55
    \stemUp %{{color()}%}  a2. ~ | \barNumberCheck #56
    \stemUp a2. \bar "|."
}

% The score definition
\score {
    <<
        \new StaffGroup
        <<
            \new Staff
            <<
                
                \context Staff << 
                    \mergeDifferentlyDottedOn\mergeDifferentlyHeadedOn
                    \context Voice = "PartPOneVoiceOne" {  \PartPOneVoiceOne }
                    >>
                >>

        >>

    >>
    \layout {}
    }

