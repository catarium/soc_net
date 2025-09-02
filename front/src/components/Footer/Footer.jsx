import { useEffect, useState } from "react";
import "./Footer.css";
import { useNavigate } from 'react-router'

function SelectSection(route) {
  useNavigate(route)
}

function Section({ text, activated, route }) {
  const navigate = useNavigate()
  let className = "FooterEl"
  if (activated === true) {
    className = "FooterEl FooterElActivated"
  }
  return (
    <>
      <div id={text} className={className} onClick={() => navigate(route)}>
        {text}
      </div>
    </>
  );
}

export default function Footer({ SectionName }) {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    async function f() {
      const res = await fetch(`/api/auth/me`);
      if (!res.ok) {
        alert(await res.text());
        return;
      }
      setUserData((await res.json()).res);
    }
    f();
  }, []);
  return (
    <>
      <div className="Footer">
        <Section text="All" route="/all" activated={'All' == SectionName}></Section>
        <Section text="Subs" route="/subs" activated={'Subs' == SectionName}></Section>
        <Section text="Profile" route={"/profile/" + (userData ? userData.id : "")} activated={'Profile' == SectionName}></Section>
      </div>
    </>
  );
}
