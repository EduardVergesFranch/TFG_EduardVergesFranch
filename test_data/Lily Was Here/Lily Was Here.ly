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

\\header {
    title = "Lily Was Here"
    }

#(set-global-staff-size 18.581589107904897)
\paper {
    
    page-breaking = #ly:one-page-breaking

    paper-width = 22.86\cm
    paper-height = 30.49\cm
    top-margin = 1.5\cm
    bottom-margin = 1.5\cm
    left-margin = 1.5\cm
    right-margin = 1.5\cm
    between-system-space = 1.5\cm
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
    \clef "treble" \numericTimeSignature\time 4/4 \key g \major
    \transposition c \break | % 1
    \tempo 4=108 %{{color()}%} <e b' e g b e>1 ~ ~ ~ ~ ~ ~ %{{ eps(110,0,5,2)}%} -\mf | % 2
     <e b' e g b e>1 | % 3
     r4 ^\markup{ \bold\small {\box "Theme I" } } \stemUp %{{color()}%}
    b''8 [ \stemUp %{{color()}%}  g8 ~ ] \stemUp g4
    \stemUp %{{color()}%}  a8 [ \stemUp %{{color()}%}  e8 ~ ] | % 4
    e1 | % 5
    %{{color()}%} <a, e' a c e>1 ~ ~ ~ ~ ~ | % 6
    <a e' a c e>1 \break | % 7
    r4 %{{ eps(110,6,9,2)}%} \stemUp %{{color()}%}  b'8 [ \stemUp %{{color()}%}
    g8 ~ ] \stemUp g4 \stemUp %{{color()}%}  a8 [
    \stemUp %{{color()}%}  fis8 ~ ] | % 8
    fis2 r8 \stemUp %{{color()}%}  g8 \stemUp %{{color()}%}
    fis8 [ \stemUp %{{color()}%}  e8 ~ ] | % 9
    e1 | % 10
    %{{color()}%} <e, b' e g b e>1 \break | % 11

    r4 %{{ eps(110,10,13,2)}%} \stemUp %{{color()}%}
    b''8 [ \stemUp %{{color()}%}  g8 ~ ] \stemUp g4
    \stemUp %{{color()}%}  a8 [ \stemUp %{{color()}%}  e8 ~ ] | % 12
    e1 | % 13
    %{{color()}%} <a, e' a c e>1 ~ ~ ~ ~ ~ | % 14
    <a e' a c e>1 \break| % 15
    r4 %{{ eps(110,14, 17,2)}%} \stemUp %{{color()}%}  b'8 [ \stemUp %{{color()}%}
    g8 ~ ] \stemUp g4 \stemUp %{{color()}%}  a8 [
    \stemUp %{{color()}%}  fis8 ~ ] | % 16
    \stemUp fis2 r8 \stemUp %{{color()}%}  g8 \stemUp %{{color()}%}
    fis8 [ \stemUp %{{color()}%}  e8 ~ ] | % 17
    e1 | %18
    %{{color()}%} <e, b' e g b e>1 \break | % 19

    r8 %{{ eps(110,18, 21,2)}%} ^\markup{ \bold\small {\box "Theme II" }
        } \stemUp %{{color()}%}  e'8 \stemDown %{{color()}%}  g8 [
    \stemDown %{{color()}%}  d'8 ~ ] \stemDown d8 \stemUp %{{color()}%}
    e,4 \stemUp %{{color()}%}  g8 ~ | % 20
    g1 | % 21
    %{{color()}%} <a, e' a c e>1 ~ ~ ~ ~ ~ | % 22
    <a e' a c e>1 \break | % 23
    r8 %{{ eps(110,22, 25,2)}%} \stemUp %{{color()}%}  e'8 \stemDown %{{color()}%}
    g8 [ \stemDown %{{color()}%}  d'8 ~ ] \stemDown d8
    \stemUp %{{color()}%}  e,4 \stemUp %{{color()}%}  a8 ~ | % 24
    \stemUp a4. \stemDown %{{color()}%}  b8 ~ \stemDown b2 | % 25
    %{{color()}%} <e,, b' e g b e>1 ~ ~ ~ ~ ~ ~ | % 26
    <e b' e g b e>1 \break  \bar "||" % 27
    r4 %{{ eps(110,26, 30,2)}%} ^\markup{ \bold\small {\box
            "Theme I" } } \stemUp %{{color()}%}  b''8 [ \stemUp %{{color()}%} 
    g8 ~ ] \stemUp g4 \stemUp %{{color()}%}  a8 [ \stemUp %{{color()}%}
    e8 ~ ] | % 28
    e1 | % 29
    %{{color()}%} <a, e' a c e>1 ~ ~ ~ ~ ~ | % 30
    <a e' a c e>1 | % 31
    r4  \stemUp %{{color()}%}  b'8 [ \stemUp %{{color()}%}
    g8 ~ ] \stemUp g4 \stemUp %{{color()}%}  a8 [ \stemUp %{{color()}%}
    fis8 ~ ] \break | % 32
    \stemUp fis2 %{{ eps(110,31, 35,2)}%} r8 \stemUp %{{color()}%}  g8 \stemUp %{{color()}%}
    fis8 [ \stemUp %{{color()}%}  e8 ~ ] | % 33
    e1 | % 34
    %{{color()}%} <d a' d fis>1 | % 35
    %{{color()}%} <e, b' e g b e>1 ~ ~ ~ ~ ~ ~ | % 36
    <e b' e g b e>1 \bar "|."
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

