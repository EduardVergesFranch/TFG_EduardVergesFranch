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
\pointAndClickOff

\header {
    tagline =  ""
    }

#(set-global-staff-size 20.004375410194708)
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
        autoBeaming = ##f
    }
}
PartPOneVoiceOne =  \relative f''{
    \clef "treble" \numericTimeSignature\time 4/4 \key f \major
    \transposition c \break | % 1
    \tempo 4=104 r8 %{{ eps(110,0, 3,2)}%} ^\markup{ \bold\small {\box "Intro" } }
    \stemDown %{{color()}%}  f8 -\mf \stemDown %{{color()}%} f8 [ \stemDown %{{color()}%} f8 ] \stemDown %{{color()}%} f8 [
    \stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8 \stemDown %{{color()}%} e8 ] | % 2
    \stemDown %{{color()}%}  e8 [ \stemDown %{{color()}%}  d8 \stemDown %{{color()}%} d8
    \stemDown %{{color()}%}  d8 ] \stemDown %{{color()}%}  d8 [\stemDown %{{color()}%}  d8 \stemDown %{{color()}%}  e8 \stemDown %{{color()}%} e8 ] | % 3
    r8 \stemDown %{{color()}%}  f8 \stemDown %{{color()}%}  f8 [\stemDown %{{color()}%}  f8 ] \stemDown %{{color()}%}  f8 [\stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8 \stemDown %{{color()}%} e8 ] | % 4
    \stemDown %{{color()}%}  e8 [ \stemDown %{{color()}%}  d8 \stemDown %{{color()}%}d8 \stemDown %{{color()}%}  d8 ]
    \stemDown %{{color()}%}  d8 [\stemDown %{{color()}%}  bes8 \stemDown %{{color()}%}  bes8 \stemDown %{{color()}%}  bes8 ] \break | % 5

    r8 %{{ eps(110,4, 7,2)}%} ^\markup{ \bold\small {\box "Verse" } }
    \stemDown %{{color()}%}  f'8 \stemDown %{{color()}%} f8 [ \stemDown %{{color()}%}  f8 ]
    \stemDown %{{color()}%}  f8
    [\stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8
    \stemDown %{{color()}%}  e8 ] | % 6
    \stemDown %{{color()}%}  e8 [ \stemDown %{{color()}%}  d8
    \stemDown %{{color()}%}  d8 \stemDown %{{color()}%}  d8 ]
    \stemDown %{{color()}%}  d8 [ \stemDown %{{color()}%}  d8
    \stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8 ] | % 7
    r8 \stemDown %{{color()}%}  f8 \stemDown %{{color()}%}  f8 [\stemDown %{{color()}%}  f8 ]
    \stemDown %{{color()}%}  f8 [ \stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8
    \stemDown %{{color()}%}  e8 ] | % 8
    \stemDown %{{color()}%}  e8 [ \stemDown %{{color()}%}  d8
    \stemDown %{{color()}%}  d8 \stemDown %{{color()}%}  d8 ]
    \stemDown %{{color()}%}  d8 [ \stemDown %{{color()}%}  bes8
    \stemDown %{{color()}%}  bes8 \stemDown %{{color()}%}  bes8 ] \break | % 9

    r8 %{{ eps(110,8,11,2)}%} ^\markup{ \bold\small {\box "Verse" } }
    \stemDown %{{color()}%}  f'8 \stemDown %{{color()}%} f8
    [ \stemDown %{{color()}%}  f8 ] \stemDown %{{color()}%}  f8 [\stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8
    \stemDown %{{color()}%}  e8 ] | % 10
    \stemDown %{{color()}%}  e8 [ \stemDown %{{color()}%}  d8
    \stemDown %{{color()}%}  d8 \stemDown %{{color()}%}  d8 ]
    \stemDown %{{color()}%}  d8 [ \stemDown %{{color()}%}  d8
    \stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8 ] | % 11
    r8 \stemDown %{{color()}%}  f8 \stemDown %{{color()}%}  f8 [ \stemDown %{{color()}%}  f8 ]
    \stemDown %{{color()}%}  f8 [ \stemDown %{{color()}%}  e8 \stemDown %{{color()}%}  e8
    \stemDown %{{color()}%}  e8 ] | % 12
    \stemDown %{{color()}%}  e8 [ \stemDown %{{color()}%}  d8 \stemDown %{{color()}%}  d8 \stemDown %{{color()}%}  d8 ]
    \stemDown %{{color()}%}  d8 [ \stemDown %{{color()}%}  bes8 \stemDown %{{color()}%}  bes8 \stemDown %{{color()}%}  bes8 ] \break | % 13

    \stemDown %{{color()}%} <d f>8 [ %{{ eps(110,12, 15,2)}%} ^\markup{\bold\small {\box "Chorus" } }
    \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ]
    \stemDown %{{color()}%} <d f>8 [ \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ] | \barNumberCheck #14
    \stemDown %{{color()}%} <d f>8 [ \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ]
    \stemDown %{{color()}%} <d f>8 [ \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ] | % 15
    \stemDown %{{color()}%} <c e>8 [ \stemDown %{{color()}%} <c e>8
    \stemDown %{{color()}%} <c e>8 \stemDown %{{color()}%} <c e>8 ]
    \stemDown %{{color()}%} <c e>8 [ \stemDown %{{color()}%} <c e>8
    \stemDown %{{color()}%} <c e>8 \stemDown %{{color()}%} <c e>8 ] | % 16
    \stemDown %{{color()}%} <b g'>8 [ \stemDown %{{color()}%} <b g'>8
    \stemDown %{{color()}%} <b g'>8 \stemDown %{{color()}%} <b g'>8]
    \stemDown %{{color()}%} <b g'>8 [ \stemDown %{{color()}%} <b g'>8 ]
    \stemDown %{{color()}%} <b g'>4 \break | % 17

    \stemDown %{{color()}%} <d f>8 [ %{{ eps(110,16,19,2)}%} ^\markup{\bold\small {\box "Chorus" } }
    \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ]
    \stemDown %{{color()}%} <d f>8 [ \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ] | \barNumberCheck #18
    \stemDown %{{color()}%} <d f>8 [ \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ]
    \stemDown %{{color()}%} <d f>8 [ \stemDown %{{color()}%} <d f>8
    \stemDown %{{color()}%} <d f>8 \stemDown %{{color()}%} <d f>8 ] | % 19
    \stemDown %{{color()}%} <c e>8 [ \stemDown %{{color()}%} <c e>8
    \stemDown %{{color()}%} <c e>8 \stemDown %{{color()}%} <c e>8 ]
    \stemDown %{{color()}%} <c e>8 [ \stemDown %{{color()}%} <c e>8
    \stemDown %{{color()}%} <c e>8 \stemDown %{{color()}%} <c e>8 ] | % 20
    \stemDown %{{color()}%} <b g'>8 [ \stemDown %{{color()}%} <b g'>8
    \stemDown %{{color()}%} <b g'>8 \stemDown %{{color()}%} <b g'>8]
    \stemDown %{{color()}%} <b g'>8 [ \stemDown %{{color()}%} <b g'>8 ]
    \stemDown %{{color()}%} <b g'>4 \break | % 21

    \stemDown %{{color()}%} <d, a' d f>2 %{{ eps(110,20, 23,2)}%} -\mp ^\markup{ \bold\small {\box "Bridge" } }
    \stemUp %{{color()}%} <c e g c e>2 | % 22
    \stemDown %{{color()}%}  bes'4 \stemDown %{{color()}%}  c4 \stemDown %{{color()}%} d4
    \stemDown %{{color()}%}  e4 | % 23
    \stemDown %{{color()}%} <d, a' d f>2 \stemUp %{{color()}%} <c e g c e>2 | % 24
    \stemDown %{{color()}%}  bes'4 \stemDown %{{color()}%}  c4 \stemDown %{{color()}%} d4 \stemDown %{{color()}%}  e4 \break | % 25

    \stemDown %{{color()}%} <d f>4 %{{ eps(110,24,27,2)}%} \stemDown %{{color()}%} <d f>4
    \stemDown %{{color()}%} <c e>4 \stemDown %{{color()}%} <c e>4 | % 26
    \stemDown %{{color()}%} <d f>4 \stemDown %{{color()}%} <d f>4
    \stemDown %{{color()}%} <d f>4 \stemDown %{{color()}%} <d f>4 | % 27
    \stemDown %{{color()}%} <d f>4 \stemDown %{{color()}%} <d f>4
    \stemDown %{{color()}%} <c e>4 \stemDown %{{color()}%} <c e>4 | \barNumberCheck #28
    \stemDown %{{color()}%} <d f>4 \stemDown %{{color()}%} <d f>4
    \stemDown %{{color()}%} <d f>4 \stemDown %{{color()}%} <d f>4 \break | % 29

    r8 %{{ eps(110,28, 31,2)}%} -\mf ^\markup{\bold\small {\box "Verse" }}
    \stemDown %{{color()}%} f8 \stemDown %{{color()}%} f8 [\stemDown %{{color()}%} f8 ]
    \stemDown %{{color()}%} f8 [\stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 ] | % 30
    \stemDown %{{color()}%}e8 [\stemDown %{{color()}%}d8 \stemDown %{{color()}%} d8 \stemDown %{{color()}%} d8 ]
    \stemDown %{{color()}%} d8 [\stemDown %{{color()}%} d8 \stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 ] | % 31
    r8 \stemDown %{{color()}%} f8 \stemDown %{{color()}%} f8 [ \stemDown %{{color()}%} f8 ]
    \stemDown %{{color()}%} f8 [\stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 ] | % 32
    \stemDown %{{color()}%} e8 [\stemDown %{{color()}%} d8 \stemDown %{{color()}%} d8 \stemDown %{{color()}%} d8 ]
    \stemDown %{{color()}%} d8 [\stemDown %{{color()}%} bes8 \stemDown %{{color()}%} bes8 \stemDown %{{color()}%} bes8 ] \break | % 33

     r8 %{{ eps(110,32, 36,2)}%}
    \stemDown %{{color()}%} f8 \stemDown %{{color()}%} f8 [ \stemDown %{{color()}%} f8 ]
    \stemDown %{{color()}%} f8 [\stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 ] | % 34
    \stemDown %{{color()}%} e8 [ \stemDown %{{color()}%} d8 \stemDown %{{color()}%} d8 \stemDown %{{color()}%} d8 ]
    \stemDown %{{color()}%} d8 [ \stemDown %{{color()}%} d8 \stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 ] | % 35
    r8 \stemDown %{{color()}%} f8 \stemDown %{{color()}%} f8 [ \stemDown %{{color()}%} f8 ] \stemDown %{{color()}%} f8 [
    \stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 \stemDown %{{color()}%} e8 ] | % 36
    \stemDown %{{color()}%} e8 [ \stemDown %{{color()}%} d8 \stemDown %{{color()}%} d8 \stemDown %{{color()}%} d8 ]
    \stemDown %{{color()}%} d8 [ \stemDown %{{color()}%} bes8 \stemDown %{{color()}%} bes8 \stemDown %{{color()}%} bes8 ]| % 37

    %{{color()}%} <d, a' d f>1 \bar "|."

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

