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
% automatically converted by musicxml2ly from ../../RP/Guitar/Grade0/Edited/GTR Gr 0 Runaway Train.xml
\pointAndClickOff

\header {
    title = "Runaway Train"
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
        skipBars = ##t
        autoBeaming = ##f
        }
    }
PartPOneVoiceOne =  \relative g {
    \clef "treble" \numericTimeSignature\time 4/4 \key c \major
    \transposition c \break | % 1
    \tempo 4=112 %{{color()}%} <g b d g b g'>1 %{{ eps(110,0, 4,3)}%} -\mf
    ^\markup{ \bold\small {\box "Intro" } } | % 2
    \stemUp %{{color()}%} <g b d g b g'>4 r4 r2 \bar "||"
    %{{color()}%} <c e g c e>1 ~ ~ ~ ~ ~ ^\markup{ \bold\small {\box
            "Verse" } } | % 4
    <c e g c e>1 | % 5
    %{{color()}%} <e, b' e g b e>1 ~ ~ ~ ~ ~ ~ \break | % 6
    <e b' e g b e>1 %{{ eps(110,5, 9,3)}%} | % 7
    %{{color()}%} <a e' a c e>1 ~ ~ ~ ~ ~ | % 8
    <a e' a c e>1 | % 9
    %{{color()}%} <g b d g b g'>1 ~ ~ ~ ~ ~ ~ | \barNumberCheck #10
    <g b d g b g'>1 \break | % 11
    \stemUp %{{color()}%} <c e g c e>4 %{{ eps(105,10, 13,3)}%} _\markup{
        \tiny\italic {So tired…} } \stemUp %{{color()}%} <c e g c e>4
    \stemUp %{{color()}%} <c e g c e>4 \stemUp %{{color()}%} <c e g c e>4 | % 12
    \stemUp %{{color()}%} <c e g c e>4 \stemUp %{{color()}%} <c e g c e>4
    \stemUp %{{color()}%} <c e g c e>4 \stemUp %{{color()}%} <c e g c e>4 | % 13
    \stemUp %{{color()}%} <e, b' e g b e>4 \stemUp %{{color()}%} <e b' e g b
        e>4 \stemUp %{{color()}%} <e b' e g b e>4 \stemUp %{{color()}%} <e
        b' e g b e>4 | % 14
    \stemUp %{{color()}%} <e b' e g b e>4 \stemUp %{{color()}%} <e b' e g b
        e>4 \stemUp %{{color()}%} <e b' e g b e>4 \stemUp %{{color()}%} <e
        b' e g b e>4 \break | % 15
    \stemUp %{{color()}%} <a e' a c e>4 %{{ eps(110,14, 17,3)}%} \stemUp
    %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4 \stemUp
    %{{color()}%} <a e' a c e>4 | % 16
    \stemUp %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4
    \stemUp %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4
    | % 17
    \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g b d g b
        g'>4 \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g
        b d g b g'>4 | % 18
    %{{color()}%} <g b d g b g'>1 \bar "||"
    \break \stemDown %{{color()}%}b'4 %{{ eps(110,18, 21,3)}%} -\f ^\markup{ \bold\small
        {\box "Pre-chorus" } } _\markup{ \tiny\italic {Seems no one can
            help me now…} } \stemDown %{{color()}%}c8 [ \stemDown %{{color()}%}c8 ~ ] \stemDown c4
    \stemDown c4 | \barNumberCheck #20
    \stemDown %{{color()}%}b4 \stemDown %{{color()}%}c8 [ \stemDown %{{color()}%}c8 ~ ] \stemDown c4 \stemDown %{{color()}%}c4 | % 21
    \stemDown %{{color()}%}b4 \stemDown %{{color()}%}c8 [ \stemDown %{{color()}%}c8 ~ ] \stemDown c4 \stemDown
    %{{color()}%}c4 | % 22
    \stemDown %{{color()}%}e4 \stemDown %{{color()}%}d4 \stemDown %{{color()}%}c4 \stemDown %{{color()}%}b4 \break | % 23
    \stemDown %{{color()}%}b4 %{{ eps(110,22, 25,3)}%} \stemDown %{{color()}%}c8 [ \stemDown %{{color()}%}c8 ~ ]
    \stemDown c4 \stemDown %{{color()}%}c4 | % 24
    \stemDown %{{color()}%}b4 \stemDown %{{color()}%}c4 \stemUp %{{color()}%}g4 \stemUp %{{color()}%}a4 | % 25
    \stemUp %{{color()}%}a4 \stemUp %{{color()}%}g8 [ \stemUp %{{color()}%}g8 ~ ] \stemUp g2 | % 26
    R1 \bar "||"
    \break \stemUp %{{color()}%} <c, e g c e>4 %{{ eps(110,26, 30,3)}%} -\mf
    ^\markup{ \bold\small {\box "Chorus" } } \stemUp %{{color()}%} <c e g
        c e>4 \stemUp %{{color()}%} <c e g c e>4 \stemUp %{{color()}%} <c e
        g c e>4 | % 28
    \stemUp %{{color()}%} <c e g c e>4 \stemUp %{{color()}%} <c e g c e>4
    \stemUp %{{color()}%} <c e g c e>4 \stemUp %{{color()}%} <c e g c e>4 | % 29
    \stemUp %{{color()}%} <e, b' e g b e>4 \stemUp %{{color()}%} <e b' e g b
        e>4 \stemUp %{{color()}%} <e b' e g b e>4 \stemUp %{{color()}%} <e
        b' e g b e>4 | \barNumberCheck #30
    \stemUp %{{color()}%} <e b' e g b e>4 \stemUp %{{color()}%} <e b' e g b
        e>4 \stemUp %{{color()}%} <e b' e g b e>4 \stemUp %{{color()}%} <e
        b' e g b e>4 | % 31
    \stemUp %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4
    \stemUp %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4
    \break | % 32
    \stemUp %{{color()}%} <a e' a c e>4 %{{ eps(110,31, 36,3)}%} \stemUp
    %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>4 \stemUp
    %{{color()}%} <a e' a c e>4 | % 33
    \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g b d g b
        g'>4 \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g
        b d g b g'>4 | % 34
    \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g b d g b
        g'>4 \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g
        b d g b g'>4 | % 35
    %{{color()}%} <g b d g b g'>1 | % 36
    \stemUp %{{color()}%} <g b d g b g'>4 r4 r2 | % 37
    %{{color()}%} <c e g c e>1 \bar "|."
    }

PartPOneVoiceOneChords =  \chordmode {
    | % 1
    g1:5 | % 2
    s4 s4 s2 \bar "||"
    c1:5 | % 4
    s1 | % 5
    e1:m | % 6
    s1 | % 7
    a1:m | % 8
    s1 | % 9
    g1:5 | \barNumberCheck #10
    s1 | % 11
    c4:5 s4 s4 s4 | % 12
    s4 s4 s4 s4 | % 13
    e4:m s4 s4 s4 | % 14
    s4 s4 s4 s4 | % 15
    a4:m s4 s4 s4 | % 16
    s4 s4 s4 s4 | % 17
    g4:5 s4 s4 s4 | % 18
    s1 \bar "||"
    f4:5 s8 s8 s4 s4 | \barNumberCheck #20
    g4:5 s8 s8 s4 s4 | % 21
    c4:5 s8 s8 s4 s4 | % 22
    a4:m s4 s4 s4 | % 23
    f4:5 s8 s8 s4 s4 | % 24
    e4:m s4 s4 s4 | % 25
    g4:5 s8 s8 s2 | % 26
    s1 \bar "||"
    c4:5 s4 s4 s4 | % 28
    s4 s4 s4 s4 | % 29
    e4:m s4 s4 s4 | \barNumberCheck #30
    s4 s4 s4 s4 | % 31
    a4:m s4 s4 s4 | % 32
    s4 s4 s4 s4 | % 33
    g4:5 s4 s4 s4 | % 34
    s4 s4 s4 s4 | % 35
    s1 | % 36
    s4 s4 s2 | % 37
    c1:5 \bar "|."
    }

% The score definition
\score {
    <<
        
        \new StaffGroup
        <<
            \context ChordNames = "PartPOneVoiceOneChords" { \PartPOneVoiceOneChords}
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
    % To create MIDI output, uncomment the following line:
    %  \midi {\tempo 4 = 100 }
    }

