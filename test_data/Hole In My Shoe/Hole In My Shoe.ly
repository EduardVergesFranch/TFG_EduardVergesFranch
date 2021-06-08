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
    title = "Hole In My Shoe"
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
PartPOneVoiceOne =  \relative b {
    \clef "treble" \numericTimeSignature\time 4/4 \key g \major
    \transposition c \break | % 1
    \tempo 4=102 \stemUp %{{color()}%}  b4 %{{ eps(110,0, 3,2)}%} -\mf
    ^\markup{ \small {[B]} } ^\markup{ \bold\small {\box "Intro" } }
    \stemUp %{{color()}%}  b4 \stemUp %{{color()}%}  b4 \stemUp %{{color()}%} 
    b4 | % 2
    \stemUp %{{color()}%}  b4 \stemUp %{{color()}%}  b4 \stemUp %{{color()}%} 
    b4 \stemUp %{{color()}%}  b4 \bar "||"
    \stemUp %{{color()}%} <g b d g b g'>4 ^\markup{ \bold\small {\box
            "Verse 1" } } \stemUp %{{color()}%} <g b d g b g'>4 \stemUp
    %{{color()}%} <g b d g b g'>8 [ \stemUp %{{color()}%} <g b d g b g'>8
    ] \stemUp %{{color()}%} <g b d g b g'>4 | % 4
    \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g b d g
        b g'>4 \stemUp %{{color()}%} <g b d g b g'>8 [ \stemUp
    %{{color()}%} <g b d g b g'>8 ] \stemUp %{{color()}%} <g b d g b g'>4
    \break | % 5
    \stemUp %{{color()}%} <a e' a c e>4 %{{ eps(110,4, 7,2)}%} \stemUp
    %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c e>8 [
    \stemUp %{{color()}%} <a e' a c e>8 ] \stemUp %{{color()}%} <a e' a
        c e>4 | % 6
    \stemUp %{{color()}%} <a e' a c e>4 \stemUp %{{color()}%} <a e' a c
        e>4 \stemUp %{{color()}%} <a e' a c e>8 [ \stemUp %{{color()}%}
    <a e' a c e>8 ] \stemUp %{{color()}%} <a e' a c e>4 | % 7
    \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g b d g
        b g'>4 \stemUp %{{color()}%} <g b d g b g'>8 [ \stemUp
    %{{color()}%} <g b d g b g'>8 ] \stemUp %{{color()}%} <g b d g b g'>4
    | % 8
    \stemUp %{{color()}%} <g b d g b g'>4 \stemUp %{{color()}%} <g b d g
        b g'>4 \stemUp %{{color()}%} <g b d g b g'>8 [ \stemUp
    %{{color()}%} <g b d g b g'>8 ] \stemUp %{{color()}%} <g b d g b g'>4
    \break | % 9
    \stemUp %{{color()}%}  bes4 %{{ eps(110,8, 12,2)}%} \stemUp %{{color()}%}
    bes4 \stemUp %{{color()}%}  bes4 \stemUp %{{color()}%}  bes4 |
    \barNumberCheck #10
     %{{color()}%} bes1 | % 11
     %{{color()}%} bes1 | % 12
    \stemUp %{{color()}%}  b4 ^\markup{ \small {B} } \stemUp %{{color()}%} 
    b4 \stemUp %{{color()}%}  b4 \stemUp %{{color()}%}  b4 | % 13
    \stemUp %{{color()}%}  b4 \stemUp %{{color()}%}  b4 \stemUp %{{color()}%} 
    b4 \stemUp %{{color()}%}  b4 \bar "||"
    \break \stemUp %{{color()}%}  g'8 [ %{{ eps(110,13, 16,2)}%} -\f
    ^\markup{ \bold\small {\box "Verse 2" } } \stemUp %{{color()}%}  a8
    \stemUp %{{color()}%}  b8 \stemUp %{{color()}%}  c8 ~ ] \stemDown
    c8 \stemDown %{{color()}%}  b4. ~ | % 15
    \stemDown %{{color()}%}  b2. r4 | % 16
    \stemDown %{{color()}%}  c8 [ \stemDown %{{color()}%}  d8 \stemDown %{{color()}%} 
    b8 \stemDown %{{color()}%}  a8 ~ ] \stemUp   a2 ~ | % 17
    \stemUp %{{color()}%}  a2. r4 \break | % 18
    \stemUp %{{color()}%}  g8 [ %{{ eps(110,17, 21,2)}%} \stemUp %{{color()}%}
    a8 \stemUp %{{color()}%}  b8 \stemUp %{{color()}%}  c8 ~ ] \stemDown
    c8 \stemDown %{{color()}%}  b4. ~ | % 19
    \stemDown b2. r4 | \barNumberCheck #20
     %{{color()}%} bes1 | % 21
     %{{color()}%} bes1 | % 22
    R1 \bar "||"
    \break %{{color()}%}  b1 ~ %{{ eps(110,22, 25,2)}%} ^\markup{
        \bold\small {\box "Instrumental" } } | % 24
    \stemDown b2 r4 \stemDown %{{color()}%}  d4 | % 25
    \stemUp %{{color()}%}  c8 [ \stemUp %{{color()}%}  b8 \stemUp %{{color()}%} 
    a8 \stemUp %{{color()}%}  a8 ~ ] \stemUp  a2 ~ | % 26
    \stemUp a2. r4 \break | % 27
     %{{color()}%} b1 ~ %{{ eps(110,26, 30,2)}%} | % 28
    \stemDown %{{color()}%}  b2 r4 \stemDown d4 | % 29
    \stemUp %{{color()}%}  c8 [ \stemUp %{{color()}%}  b8 \stemUp %{{color()}%} 
    a8 \stemUp %{{color()}%}  a8 ~ ] \stemUp a2 |
    \barNumberCheck #30
    %{{color()}%} <d, a' d fis>1 | % 31
    %{{color()}%} <g, b d g b g'>1 \bar "|."
    }

PartPOneVoiceOneChords =  \chordmode {
    | % 1
    s4 s4 s4 s4 | % 2
    s4 s4 s4 s4 \bar "||"
    g4:5 s4 s8 s8 s4 | % 4
    s4 s4 s8 s8 s4 | % 5
    a4:m s4 s8 s8 s4 | % 6
    s4 s4 s8 s8 s4 | % 7
    g4:5 s4 s8 s8 s4 | % 8
    s4 s4 s8 s8 s4 | % 9
    bes4:5 s4 s4 s4 |
    s1 | % 11
    s1 | % 12
    s4 s4 s4 s4 | % 13
    s4 s4 s4 s4 \bar "||"
    g8:5 s8 s8 s8 s8 s4. | % 15
    s2. s4 | % 16
    a8:m s8 s8 s8 s2 | % 17
    s2. s4 | % 18
    g8:5 s8 s8 s8 s8 s4. | % 19
    s2. s4 | \barNumberCheck #20
    bes1:5 | % 21
    s1 | % 22
    s1 \bar "||"
    g1:5 | % 24
    s2 s4 s4 | % 25
    f8:5 s8 s8 s8 s2 | % 26
    d2.:5 s4 | % 27
    g1:5 | % 28
    s2 s4 s4 | % 29
    f8:5 s8 s8 s8 s2 |
    d1:5 | % 31
    g1:5 \bar "|."
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

  }

