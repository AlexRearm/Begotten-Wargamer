<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<gameSystem xmlns="http://www.battlescribe.net/schema/gameSystemSchema"
            id="a1b2c3d4-0000-4000-8000-000000000001" name="Врата" revision="1" battleScribeVersion="2.03"
            hidden="false">
  <readme>Домашняя игровая система «Врата». Данные генерируются из codex.json.</readme>
  <profileTypes>
    <profileType id="5e394dae-2d39-4e75-842f-67ab39e37214" name="Unit">
      <characteristicTypes>
        <characteristicType id="c84dc8ca-3a32-4867-8f0d-492720092c81" name="M"/>
        <characteristicType id="a21cb80a-e1e4-479a-8549-cf45d45b2f1d" name="T"/>
        <characteristicType id="d23daa50-ddfb-48a0-8a65-b6ea1e1fac04" name="Sv"/>
        <characteristicType id="78442223-36d8-44d4-8967-8a0c930ab2ca" name="InSv"/>
        <characteristicType id="6ba7776c-9ed0-4148-879c-070517358840" name="W"/>
        <characteristicType id="af09b0ef-7c4b-4930-8f11-e7c4bec68087" name="LD"/>
        <characteristicType id="c728968e-737b-4761-8d6a-ec1b41f096d1" name="OC"/>
      </characteristicTypes>
    </profileType>
    <profileType id="93726c05-ab82-4a52-8393-8c175e2bda48" name="Ranged Weapon">
      <characteristicTypes>
        <characteristicType id="484e1a4b-24ee-4c76-8031-36444380bc5c" name="Range"/>
        <characteristicType id="9d919dca-041d-4558-8999-2ec7a93a3051" name="A"/>
        <characteristicType id="533fbbe5-c7a7-4fc0-87cb-dee784341215" name="Skill"/>
        <characteristicType id="b41a74d4-b711-4597-8321-b4598492122c" name="S"/>
        <characteristicType id="364c7262-ad89-4636-8fc6-6795931c1c85" name="AP"/>
        <characteristicType id="0a89b98c-f9db-4f13-84e8-1e718bde0391" name="D"/>
        <characteristicType id="717281af-e661-40be-8680-8e19e9db4486" name="Special"/>
      </characteristicTypes>
    </profileType>
    <profileType id="2a2a85d4-0058-4e94-805e-c6f3c57aac79" name="Melee Weapon">
      <characteristicTypes>
        <characteristicType id="179c0188-df38-4fb8-8bda-565c5f27c09c" name="A"/>
        <characteristicType id="a6040ed1-8078-431d-8e64-d8e9dcb9bf48" name="Skill"/>
        <characteristicType id="0cb783ab-aaa8-4ee1-8fc8-c5591407a410" name="S"/>
        <characteristicType id="7cd6cf2c-bda7-4bcc-833b-4b96b0c25f70" name="AP"/>
        <characteristicType id="84a9e346-6b11-44ca-8710-bf27fe104e7a" name="D"/>
        <characteristicType id="de03ba29-befc-43b3-85be-fa54ec440e90" name="Special"/>
      </characteristicTypes>
    </profileType>
  </profileTypes>
  <costTypes>
    <costType id="04d69444-c218-4681-8ef1-7902c6cd85ed" name="pts" defaultCostLimit="0" hidden="false"/>
  </costTypes>
  <categoryEntries>
    <categoryEntry id="325c828d-3c27-4d18-8da3-794b655dc832" name="Орден Привратников" hidden="false"/>
    <categoryEntry id="37c4e4d8-eb1b-4523-85d2-35db13b06bc0" name="Пехота" hidden="false"/>
    <categoryEntry id="ceca7fb2-b4e7-430d-896e-25bf8a6e01fe" name="Стрелки" hidden="false"/>
    <categoryEntry id="61cbe4ac-c7af-4ae3-83c1-2450bfb0fadc" name="Привратники" hidden="false"/>
    <categoryEntry id="be3d80d2-cda5-45fd-8da0-7f735c9b3259" name="Основа" hidden="false"/>
    <categoryEntry id="12f3421e-3301-42d9-89fb-36cea1dd5d5c" name="Тяжёлая" hidden="false"/>
    <categoryEntry id="ccf27112-0d2b-4db6-86e4-e9a7074a2209" name="Рыцари" hidden="false"/>
    <categoryEntry id="64c46708-c7d1-4579-8a3c-b9fedc7140ec" name="Дети Сатаны" hidden="false"/>
    <categoryEntry id="64c46708-c7d1-4579-8a3c-b9fedc7140ec" name="Дети Сатаны" hidden="false"/>
    <categoryEntry id="93d678a6-05dd-4a22-8734-624e0899a28c" name="Дом Вараздат" hidden="false"/>
    <categoryEntry id="c55a3372-5c10-49da-8699-79794893a990" name="Дом Филимаксио" hidden="false"/>
    <categoryEntry id="3c6a15e6-0ed3-4293-8778-6ebbb6a4fe9b" name="Юстициары" hidden="false"/>
  </categoryEntries>
  <forceEntries>
    <forceEntry id="abc31237-ed38-45dc-8efb-f222cbbd1a89" name="Армия" hidden="false">
      <categoryLinks>
        <categoryLink id="10072f3e-13f0-4428-8640-3fd903731417" targetId="325c828d-3c27-4d18-8da3-794b655dc832" hidden="false" primary="true"/>
      </categoryLinks>
    </forceEntry>
  </forceEntries>
</gameSystem>
