import streamlit as st
import pandas as pd

from automata.enfa import ENFA
from automata.nfa import NFA
from automata.dfa import DFA
from automata.minimizer import minimize_dfa
from automata.regex_parser import to_postfix
from utils.visualization import automaton_graph, transition_rows

st.set_page_config(page_title="AutomataFlow", page_icon="🔁", layout="wide")

st.title("🔁 AutomataFlow")
st.subheader("Regular Expression → ε-NFA → NFA → DFA → Minimized DFA")
st.write("An interactive visualizer for regular languages and finite automata.")

with st.sidebar:
    st.header("Regex input")
    regex = st.text_input("Enter regular expression", value="(a|b)*abb")
    st.caption("Operators: | union, concatenation, * Kleene star, + one-or-more, ? optional, () grouping, ε empty string.")
    build = st.button("Generate Automata", type="primary", use_container_width=True)

if "built_regex" not in st.session_state:
    st.session_state.built_regex = None

if build:
    try:
        postfix = to_postfix(regex)
        enfa = ENFA.from_regex(regex)
        nfa = NFA.from_enfa(enfa)
        dfa = DFA.from_nfa(nfa)
        minimized = minimize_dfa(dfa)
        st.session_state.machine_data = (postfix, enfa, nfa, dfa, minimized)
        st.session_state.built_regex = regex
        st.session_state.error = None
    except Exception as exc:
        st.session_state.error = str(exc)
        st.session_state.machine_data = None

if st.session_state.get("error"):
    st.error(st.session_state.error)

if st.session_state.get("machine_data"):
    postfix, enfa, nfa, dfa, minimized = st.session_state.machine_data
    st.success(f"Automata generated for: `{st.session_state.built_regex}`")
    st.caption("Postfix notation: " + " ".join(postfix))

    tabs = st.tabs(["ε-NFA", "NFA", "DFA", "Minimized DFA", "String Testing", "Comparison"])
    with tabs[0]:
        st.markdown("### ε-NFA — Thompson's Construction")
        st.graphviz_chart(automaton_graph(enfa, "ε-NFA").source, use_container_width=True)
        st.dataframe(pd.DataFrame(transition_rows(enfa)).fillna(""), use_container_width=True)
        st.write(f"Start state: **{enfa.start}** · Accept state: **{enfa.accept}** · States: **{len(enfa.states)}")
    with tabs[1]:
        st.markdown("### NFA — ε-transitions eliminated")
        st.graphviz_chart(automaton_graph(nfa, "NFA").source, use_container_width=True)
        st.dataframe(pd.DataFrame(transition_rows(nfa)).fillna(""), use_container_width=True)
        st.write(f"Accept states: **{sorted(nfa.accepts)}** · States: **{len(nfa.states)}")
    with tabs[2]:
        st.markdown("### DFA — Subset Construction")
        st.graphviz_chart(automaton_graph(dfa, "DFA").source, use_container_width=True)
        st.dataframe(pd.DataFrame(transition_rows(dfa)).fillna(""), use_container_width=True)
        st.write(f"Accept states: **{sorted(dfa.accepts)}** · States: **{len(dfa.states)}")
        st.caption("DFA state labels represent sets of NFA states.")
    with tabs[3]:
        st.markdown("### Minimized DFA")
        st.graphviz_chart(automaton_graph(minimized, "Minimized DFA").source, use_container_width=True)
        st.dataframe(pd.DataFrame(transition_rows(minimized)).fillna(""), use_container_width=True)
        st.write(f"Accept states: **{sorted(minimized.accepts)}** · States: **{len(minimized.states)}")
        st.caption("State labels show the original completed-DFA states merged into each minimized state.")
    with tabs[4]:
        st.markdown("### Test strings")
        test_string = st.text_input("String to test (empty string is allowed)", key="test_string")
        if st.button("Test String"):
            accepted, path, message = minimized.run(test_string)
            if accepted:
                st.success("ACCEPTED ✓")
            else:
                st.error("REJECTED ✗")
            st.write("State path: " + " → ".join(map(str, path)))
            if message:
                st.info(message)
        st.caption("To test the empty string, leave the field blank.")
    with tabs[5]:
        st.markdown("### DFA size comparison")
        col1, col2, col3 = st.columns(3)
        col1.metric("DFA states", len(dfa.states))
        col2.metric("Minimized DFA states", len(minimized.states))
        col3.metric("States reduced", len(dfa.states) - len(minimized.states))
        st.write("Both automata recognize the same regular language; minimization removes unreachable and equivalent states.")
else:
    st.info("Enter a regular expression in the sidebar and click **Generate Automata** to begin.")
    st.markdown("#### Example expressions")
    st.code("(a|b)*abb\n(a|b)*\na(b|c)*\n0(0|1)*\na+b?")
