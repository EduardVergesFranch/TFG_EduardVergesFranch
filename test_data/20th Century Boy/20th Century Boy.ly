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
    title = "20th Century Boy"
    composer = "Guitar Grade 0"
    }

#(set-global-staff-size 20.004375410194708)
\paper {
    
    page-breaking = #ly:one-page-breaking

    paper-width = 22.86\cm
    paper-height = 30.47\cm
    top-margin = 1.49\cm
    bottom-margin = 1.49\cm
    left-margin = 1.00\cm
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
PartPOneVoiceOne =  \relative e {

    \clef "treble" \numericTimeSignature\time 4/4 \key e \major
    \transposition c \break | % 1
    \tempo 4=130

    \stemUp %{{color()}%}  e4 %{{ eps(110,0, 3,2)}%} -\f ^\markup{ \bold\small {\box "Intro" } }
    r8 \stemUp %{{color()}%}e8 \stemUp %{{color()}%}  g8 [ \stemUp %{{color()}%}  e8 ] r8
    \stemUp %{{color()}%}  g8 ~ | % 2
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%} g4 \stemUp %{{color()}%}  e4 r4 | % 3
    \stemUp %{{color()}%}  e4 r8 \stemUp %{{color()}%}  e8 \stemUp %{{color()}%}g8
     [ \stemUp %{{color()}%}  e8 ] r8 \stemUp %{{color()}%}  g8 ~ | % 4
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%} g4 \stemUp %{{color()}%}  e4 r4 \break | % 5

    \stemUp %{{color()}%}  e4 %{{ eps(110,4, 7,2)}%}
    r8 \stemUp %{{color()}%} e8 \stemUp %{{color()}%}  g8 [ \stemUp %{{color()}%}  e8 ] r8
    \stemUp %{{color()}%}  g8 ~ | % 6
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%} g4 \stemUp %{{color()}%}  e4 r4 | % 7
    \stemUp %{{color()}%}  e4 r8 \stemUp %{{color()}%}  e8 \stemUp %{{color()}%} g8 [ \stemUp %{{color()}%}  e8 ] r8 \stemUp %{{color()}%}  g8 ~| % 8
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%}g4 \stemUp %{{color()}%}  e4 r4 \break | % 9

    \stemUp %{{color()}%} <a e'>4 %{{ eps(110,8, 11,2)}%} -\mf ^\markup{ \bold\small {\box "Verse" } }
    r8 \stemUp %{{color()}%}<a e'>8 \stemUp %{{color()}%} <a e'>4 r4 | % 10
    \stemUp %{{color()}%}<a e'>4 r8 \stemUp %{{color()}%} <a e'>8
    \stemUp %{{color()}%} <a e'>4 r4 | % 11
    \stemUp %{{color()}%} <a e'>4 r8 \stemUp %{{color()}%} <a e'>8
    \stemUp %{{color()}%} <a e'>4 r4 | % 12
    \stemUp %{{color()}%} <a e'>4 r8 \stemUp %{{color()}%} <a e'>8
    \stemUp %{{color()}%} <a e'>4 \stemUp %{{color()}%}  g4 \break | % 13
    \stemUp %{{color()}%}  e4 %{{ eps(110,12, 15,2)}%} r8 \stemUp %{{color()}%}e8 \stemUp %{{color()}%}  g8 [ \stemUp %{{color()}%}  e8 ] r8
    \stemUp %{{color()}%}  g8 ~ | %14
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%}g4 \stemUp %{{color()}%}  e4 r4 | % 15
    \stemUp %{{color()}%}e4 r8 \stemUp %{{color()}%}  e8 \stemUp %{{color()}%}g8 [ \stemUp %{{color()}%}  e8 ] r8 \stemUp %{{color()}%}  g8 ~| % 16
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%}g4 \stemUp %{{color()}%}  e4 r4 \break | % 17

    \stemUp %{{color()}%} <a e'>4 %{{ eps(110,16,19,2)}%}r8
    \stemUp %{{color()}%} <a e'>8 \stemUp %{{color()}%} <a e'>4 r4 | % 18
    \stemUp %{{color()}%} <a e'>4 r8 \stemUp %{{color()}%} <a e'>8
    \stemUp %{{color()}%} <a e'>4 r4 | % 19
    \stemUp %{{color()}%} <a e'>4 r8 \stemUp %{{color()}%} <a e'>8
    \stemUp %{{color()}%} <a e'>4 r4 | % 20
    \stemUp %{{color()}%} <a e'>4 r8 \stemUp %{{color()}%} <a e'>8
    \stemUp %{{color()}%} <a e'>4 \stemUp %{{color()}%} g4
    \break | % 21

    \stemUp %{{color()}%}  e4 %{{eps(110,20,23,2)}%}
    r8 \stemUp %{{color()}%} e8 \stemUp %{{color()}%}  g8 [ \stemUp %{{color()}%}  e8 ] r8
    \stemUp %{{color()}%}  g8 ~ | % 22
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%} g4 \stemUp %{{color()}%}  e4 r4 | % 23
    \stemUp %{{color()}%}  e4 r8 \stemUp %{{color()}%}  e8 \stemUp %{{color()}%}g8 [ \stemUp %{{color()}%}  e8 ] r8 \stemUp %{{color()}%}  g8 ~ | % 24
    \stemUp g8 [ \stemUp %{{color()}%}  e8 ] \stemUp %{{color()}%}g4 \stemUp %{{color()}%}  e4 r4 \break | % 25

    \stemUp %{{color()}%} <a e'>2. %{{ eps(110,24, 27,2)}%} \stemUp %{{color()}%} <a e'>4| % 26
    \stemUp %{{color()}%}  b2. ^\markup{ \small {B5} } \stemUp %{{color()}%} b4 | % 27
    \stemUp %{{color()}%} <e, b'>8 [ \stemUp %{{color()}%} <e b'>8
    \stemUp %{{color()}%} <e b'>8 \stemUp %{{color()}%} <e b'>8 ]
    \stemUp %{{color()}%} <e b'>8 [ \stemUp %{{color()}%} <e b'>8
    \stemUp %{{color()}%} <e b'>8 \stemUp %{{color()}%} <e b'>8 ] | % 28
    \stemUp %{{color()}%} <e b'>8 [ \stemUp %{{color()}%} <e b'>8
    \stemUp %{{color()}%} <e b'>8 \stemUp %{{color()}%} <e b'>8 ]
    \stemUp %{{color()}%} <e b'>4 \stemUp %{{color()}%} <e b'>4  \break| % 29

    %{{color()}%} <e b' e gis b e>1 ~ ~ ~ ~ ~ ~ %{{ eps(110,28,31,2)}%} -\f ^\markup{ \bold\small {\box "Chorus" } } | % 30
    <e b' e gis b e>1 | % 31
    %{{color()}%} <e b' e gis b e>1 ~ ~ ~ ~ ~ ~ | % 32
    <e b' e gis b e>1   \break | % 33

    %{{color()}%} <e b' e gis b e>1 ~ ~ ~ ~ ~ ~ %{{ eps(110,32,35,2)}%}| % 34
    <e b' e gis b e>1 | % 35
    %{{color()}%} <e b' e gis b e>1 ~ ~ ~ ~ ~ ~ | % 36
    <e b' e gis b e>1 \break | % 37

    \stemUp %{{color()}%} <e b' e gis b e>4 %{{ eps(110,36,37,2)}%}
    \stemUp %{{color()}%} <e b' e gis b e>4 \stemUp %{{color()}%} <e b'
        e gis b e>4 \stemUp %{{color()}%} <e b' e gis b e>4 | % 38
    \stemUp %{{color()}%} <e b' e gis b e>4 r4 r2 \bar "|."
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

