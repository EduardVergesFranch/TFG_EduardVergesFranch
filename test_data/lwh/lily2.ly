{% macro color() -%}
     \override NoteHead.color = #(rgb-color%{ next_color() %})
{%- endmacro %}
{% macro size() -%}
     \override NoteHead.font-size = #%{next_size() %}
{%- endmacro %}
{% macro eps(scale, first_bar, last_bar, w) -%}
_\markup {
  \general-align #Y #DOWN {
    \epsfile #X #%{scale%} #"%{ eps_waveform(first_bar, last_bar, w=w*5, h=0.5, right_border_shift=0) %}"
  }
}
{%- endmacro %}
\pointAndClickOff
\header {
    tagline =  ""
    }

#(set-global-staff-size 18.581589107904897)
\paper {
    
    paper-width = 22.86\cm
    paper-height = 30\cm
    top-margin = 1.5\cm
    bottom-margin = 1.5\cm
    left-margin = 1.5\cm
    right-margin = 1.5\cm
    between-system-space = 1.5\cm
    ragged-right = ##t }
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
PartPOneVoiceOne =  \relative e {
    \clef "treble" \numericTimeSignature\time 4/4 \key g \major
    \transposition c \break | % 1
    \tempo 4=108 %{color()%} %{size()%} <e b' e g b e>1 %{eps(110,0, 5, 1)%} -\mf  ~ ~ ~ ~ ~ ~ | % 2
    <e b' e g b e>1
        | % 3
        r4 ^\markup{ \bold\small {\box "Theme I" } } \stemUp %{color()%} %{size()%} b''8 [
        \stemUp %{color()%} %{size()%} g8 ~ ] \stemUp g4 \stemUp %{color()%} %{size()%} a8 [ \stemUp %{color()%} %{size()%} e8 ~ ] | % 4
        e1 | % 5
        %{color()%} %{size()%} <a, e' a c e>1 ~ ~ ~ ~ ~ | % 6
        <a e' a c e>1 \break | % 7
        r4 %{eps(110,6,9, 1)%} \stemUp %{color()%} %{size()%} b'8 [ \stemUp %{color()%} %{size()%} g8 ~ ] \stemUp g4
        \stemUp %{color()%} %{size()%} a8 [ \stemUp %{color()%} %{size()%} fis8 ~ ] | % 8
        \stemUp fis2 r8 \stemUp %{color()%} %{size()%} g8 \stemUp %{color()%} %{size()%} fis8 [ \stemUp %{color()%} %{size()%} e8 ~ ] | % 9
        e1 | \barNumberCheck #10
        %{color()%} %{size()%} <e, b' e g b e>1 \bar "|."
    }

PartPOneVoiceOneChords =  \chordmode {
    | % 1
    e1:m | % 2
    s1
        | % 3
        e4:m s8 s8 s4 s8 s8 | % 4
        s1 | % 5
        a1:m | % 6
        s1 | % 7
        d4 s8 s8 s4 s8 s8 | % 8
        s2 s8 s8 s8 s8 | % 9
        e1:m | \barNumberCheck #10
        s1\bar "|."
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
