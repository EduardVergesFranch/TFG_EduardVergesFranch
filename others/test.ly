\version "2.20.0"
%{ from 'lily_port_macros.j2' import eps with context %} %{ from
    'lily_port_macros.j2' import eps_rh with context %} %{ from
    'lily_port_macros.j2' import eps_lh with context %}
% automatically converted by musicxml2ly from /home/eduard/Escritorio/TrinityPipeline/RP/Guitar/Grade0/Edited/GTR Gr 0 Runaway Train.xml
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
        skipBars = ##t
        autoBeaming = ##f
        }
    }
PartPOneVoiceOne =  \relative g {
    \clef "treble" \numericTimeSignature\time 4/4 \key c \major
    \transposition c \break | % 1
    \tempo 4=112 <g b d g b g'>1 %{{ eps(0, 5)}%} -\mf ^\markup{
        \bold\small {\box "Intro" } } | % 2
    \stemUp <g b d g b g'>4 r4 r2 \bar "||"
    <c e g c e>1 ~ ~ ~ ~ ~ ^\markup{ \bold\small {\box "Verse" } } | % 4
    <c e g c e>1 | % 5
    <e, b' e g b e>1 ~ ~ ~ ~ ~ ~ \break | % 6
    <e b' e g b e>1 %{{ eps(5, 10)}%} | % 7
    <a e' a c e>1 ~ ~ ~ ~ ~ | % 8
    <a e' a c e>1 | % 9
    <g b d g b g'>1 ~ ~ ~ ~ ~ ~ | \barNumberCheck #10
    <g b d g b g'>1 \break | % 11
    \stemUp <c e g c e>4 %{{ eps(10, 14)}%} _\markup{ \tiny\italic {So
            tired…} } \stemUp <c e g c e>4 \stemUp <c e g c e>4 \stemUp
    <c e g c e>4 | % 12
    \stemUp <c e g c e>4 \stemUp <c e g c e>4 \stemUp <c e g c e>4
    \stemUp <c e g c e>4 | % 13
    \stemUp <e, b' e g b e>4 \stemUp <e b' e g b e>4 \stemUp <e b' e g b
        e>4 \stemUp <e b' e g b e>4 | % 14
    \stemUp <e b' e g b e>4 \stemUp <e b' e g b e>4 \stemUp <e b' e g b
        e>4 \stemUp <e b' e g b e>4 \break | % 15
    \stemUp <a e' a c e>4 %{{ eps(14, 18)}%} \stemUp <a e' a c e>4
    \stemUp <a e' a c e>4 \stemUp <a e' a c e>4 | % 16
    \stemUp <a e' a c e>4 \stemUp <a e' a c e>4 \stemUp <a e' a c e>4
    \stemUp <a e' a c e>4 | % 17
    \stemUp <g b d g b g'>4 \stemUp <g b d g b g'>4 \stemUp <g b d g b
        g'>4 \stemUp <g b d g b g'>4 | % 18
    <g b d g b g'>1 \bar "||"
    \break \stemDown b'4 %{{ eps(18, 22)}%} -\f ^\markup{ \bold\small
        {\box "Pre-chorus" } } _\markup{ \tiny\italic {Seems no one can
            help me now…} } \stemDown c8 [ \stemDown c8 ~ ] \stemDown c4
    \stemDown c4 | \barNumberCheck #20
    \stemDown b4 \stemDown c8 [ \stemDown c8 ~ ] \stemDown c4 \stemDown
    c4 | % 21
    \stemDown b4 \stemDown c8 [ \stemDown c8 ~ ] \stemDown c4 \stemDown
    c4 | % 22
    \stemDown e4 \stemDown d4 \stemDown c4 \stemDown b4 \break | % 23
    \stemDown b4 %{{ eps(22, 26)}%} \stemDown c8 [ \stemDown c8 ~ ]
    \stemDown c4 \stemDown c4 | % 24
    \stemDown b4 \stemDown c4 \stemUp g4 \stemUp a4 | % 25
    \stemUp a4 \stemUp g8 [ \stemUp g8 ~ ] \stemUp g2 | % 26
    R1 \bar "||"
    \break \stemUp <c, e g c e>4 %{{ eps(26, 31)}%} -\mf ^\markup{
        \bold\small {\box "Chorus" } } \stemUp <c e g c e>4 \stemUp <c e
        g c e>4 \stemUp <c e g c e>4 | % 28
    \stemUp <c e g c e>4 \stemUp <c e g c e>4 \stemUp <c e g c e>4
    \stemUp <c e g c e>4 | % 29
    \stemUp <e, b' e g b e>4 \stemUp <e b' e g b e>4 \stemUp <e b' e g b
        e>4 \stemUp <e b' e g b e>4 | \barNumberCheck #30
    \stemUp <e b' e g b e>4 \stemUp <e b' e g b e>4 \stemUp <e b' e g b
        e>4 \stemUp <e b' e g b e>4 | % 31
    \stemUp <a e' a c e>4 \stemUp <a e' a c e>4 \stemUp <a e' a c e>4
    \stemUp <a e' a c e>4 \break | % 32
    \stemUp <a e' a c e>4 %{{ eps(31, 37)}%} \stemUp <a e' a c e>4
    \stemUp <a e' a c e>4 \stemUp <a e' a c e>4 | % 33
    \stemUp <g b d g b g'>4 \stemUp <g b d g b g'>4 \stemUp <g b d g b
        g'>4 \stemUp <g b d g b g'>4 | % 34
    \stemUp <g b d g b g'>4 \stemUp <g b d g b g'>4 \stemUp <g b d g b
        g'>4 \stemUp <g b d g b g'>4 | % 35
    <g b d g b g'>1 | % 36
    \stemUp <g b d g b g'>4 r4 r2 | % 37
    <c e g c e>1 \bar "|."
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

PartPTwoVoiceOne =  \relative g, {
    \clef "None" \numericTimeSignature\time 4/4 \key c \major \stopStaff
    \override Staff.StaffSymbol.line-count = #6 \startStaff \break | % 1
    <g b d g b g'>1 \6 \5 \4 \3 \2 \1 %{{ eps(0, 5)}%} | % 2
    \stemUp <g b d g b g'>4 \6 \5 \4 \3 \2 \1 r4 r2 \bar "||"
    <c e g c e>1 ~ \5 ~ \4 ~ \3 ~ \2 ~ \1 s1 | % 5
    <e, b' e g b e>1 ~ \6 ~ \5 ~ \4 ~ \3 ~ \2 ~ \1 \break | % 6
    s1 %{{ eps(5, 10)}%} | % 7
    <a e' a c e>1 ~ \5 ~ \4 ~ \3 ~ \2 ~ \1 s1 | % 9
    <g b d g b g'>1 ~ \6 ~ \5 ~ \4 ~ \3 ~ \2 ~ \1 s1 \break | % 11
    \stemUp <c e g c e>4 \5 \4 \3 \2 \1 %{{ eps(10, 14)}%} \stemUp <c e
        g c e>4 \5 \4 \3 \2 \1 \stemUp <c e g c e>4 \5 \4 \3 \2 \1
    \stemUp <c e g c e>4 \5 \4 \3 \2 \1 | % 12
    \stemUp <c e g c e>4 \5 \4 \3 \2 \1 \stemUp <c e g c e>4 \5 \4 \3 \2
    \1 \stemUp <c e g c e>4 \5 \4 \3 \2 \1 \stemUp <c e g c e>4 \5 \4 \3
    \2 \1 | % 13
    \stemUp <e, b' e g b e>4 \6 \5 \4 \3 \2 \1 \stemUp <e b' e g b e>4
    \6 \5 \4 \3 \2 \1 \stemUp <e b' e g b e>4 \6 \5 \4 \3 \2 \1 \stemUp
    <e b' e g b e>4 \6 \5 \4 \3 \2 \1 | % 14
    \stemUp <e b' e g b e>4 \6 \5 \4 \3 \2 \1 \stemUp <e b' e g b e>4 \6
    \5 \4 \3 \2 \1 \stemUp <e b' e g b e>4 \6 \5 \4 \3 \2 \1 \stemUp <e
        b' e g b e>4 \6 \5 \4 \3 \2 \1 \break | % 15
    \stemUp <a e' a c e>4 \5 \4 \3 \2 \1 %{{ eps(14, 18)}%} \stemUp <a
        e' a c e>4 \5 \4 \3 \2 \1 \stemUp <a e' a c e>4 \5 \4 \3 \2 \1
    \stemUp <a e' a c e>4 \5 \4 \3 \2 \1 | % 16
    \stemUp <a e' a c e>4 \5 \4 \3 \2 \1 \stemUp <a e' a c e>4 \5 \4 \3
    \2 \1 \stemUp <a e' a c e>4 \5 \4 \3 \2 \1 \stemUp <a e' a c e>4 \5
    \4 \3 \2 \1 | % 17
    \stemUp <g b d g b g'>4 \6 \5 \4 \3 \2 \1 \stemUp <g b d g b g'>4 \6
    \5 \4 \3 \2 \1 \stemUp <g b d g b g'>4 \6 \5 \4 \3 \2 \1 \stemUp <g
        b d g b g'>4 \6 \5 \4 \3 \2 \1 | % 18
    <g b d g b g'>1 \6 \5 \4 \3 \2 \1 \bar "||"
    \break \stemUp b'4 \2 %{{ eps(18, 22)}%} \stemUp c8 \2 \stemUp c8 ~
    \2 s4 \stemUp c4 \2 | \barNumberCheck #20
    \stemUp b4 \2 \stemUp c8 \2 \stemUp c8 ~ \2 s4 \stemUp c4 \2 | % 21
    \stemUp b4 \2 \stemUp c8 \2 \stemUp c8 ~ \2 s4 \stemUp c4 \2 | % 22
    \stemUp e4 \1 \stemUp d4 \2 \stemUp c4 \2 \stemUp b4 \2 \break | % 23
    \stemUp b4 \2 %{{ eps(22, 26)}%} \stemUp c8 \2 \stemUp c8 ~ \2 s4
    \stemUp c4 \2 | % 24
    \stemUp b4 \2 \stemUp c4 \2 \stemUp g4 \3 \stemUp a4 \3 | % 25
    \stemUp a4 \3 \stemUp g8 \3 \stemUp g8 ~ \3 s2 | % 26
    R1 \bar "||"
    \break \stemUp <c, e g c e>4 \5 \4 \3 \2 \1 %{{ eps(26, 31)}%}
    \stemUp <c e g c e>4 \5 \4 \3 \2 \1 \stemUp <c e g c e>4 \5 \4 \3 \2
    \1 \stemUp <c e g c e>4 \5 \4 \3 \2 \1 | % 28
    \stemUp <c e g c e>4 \5 \4 \3 \2 \1 \stemUp <c e g c e>4 \5 \4 \3 \2
    \1 \stemUp <c e g c e>4 \5 \4 \3 \2 \1 \stemUp <c e g c e>4 \5 \4 \3
    \2 \1 | % 29
   }
