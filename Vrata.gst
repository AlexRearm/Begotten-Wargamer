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
    <categoryEntry id="93d678a6-05dd-4a22-8734-624e0899a28c" name="Дом Вараздат" hidden="false"/>
    <categoryEntry id="c55a3372-5c10-49da-8699-79794893a990" name="Дом Филимаксио" hidden="false"/>
    <categoryEntry id="3c6a15e6-0ed3-4293-8778-6ebbb6a4fe9b" name="Юстициары" hidden="false"/>
  </categoryEntries>
  <forceEntries>
    <forceEntry id="abc31237-ed38-45dc-8efb-f222cbbd1a89" name="Армия" hidden="false">
      <categoryLinks>
        <categoryLink id="10072f3e-13f0-4428-8640-3fd903731417" targetId="325c828d-3c27-4d18-8da3-794b655dc832" hidden="false" primary="true">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="3ca2a797-ca2e-4bc6-8de7-1807096aeeff" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="96a1ffcd-60e3-450b-84a0-34970b99d569" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="e7aaead8-6e6d-46d2-89e3-2b0d59c8aee5" targetId="37c4e4d8-eb1b-4523-85d2-35db13b06bc0" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="159e8166-acee-4108-88c2-8ad04776535e" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="7fe3c3a2-a1d0-49dd-8cae-3a0b30c85a2c" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="ca92a11c-be34-4428-8841-1daa3db10410" targetId="ceca7fb2-b4e7-430d-896e-25bf8a6e01fe" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="70f44d27-2e76-4f2c-828d-60b5dbfebd54" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="4c49a468-f940-4fca-8c4d-ea4336efc716" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="545b2db1-ae16-4c82-861d-503ecc33eebd" targetId="61cbe4ac-c7af-4ae3-83c1-2450bfb0fadc" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="1a40fa52-560c-447b-81ad-6af2881fa194" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="8c7f2316-10b5-4c6a-8ee8-c0845d021035" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="5d632b6f-2490-40b3-80e4-e6cfe48536a8" targetId="be3d80d2-cda5-45fd-8da0-7f735c9b3259" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="9ab64f58-250d-4a91-868a-60a97401c6eb" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="55a805b2-7255-478d-8028-377b6e13bfff" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="3fd4d480-a39d-4aa5-8670-b9788a1d4645" targetId="12f3421e-3301-42d9-89fb-36cea1dd5d5c" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="6ba47483-c2a4-4d3a-803a-483c30e8fca4" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="56b9523f-344f-444e-8d62-79ef456b93d4" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="6f7d3c20-7aa8-45f4-8b3e-26bcf9fb313a" targetId="ccf27112-0d2b-4db6-86e4-e9a7074a2209" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="846d13a5-e7a9-4621-8a82-7f47bf337728" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="131c452e-c527-4712-84c6-629cdf8ad32b" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="017646aa-1341-4ff0-8cdf-97548dca4abf" targetId="64c46708-c7d1-4579-8a3c-b9fedc7140ec" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="2cf14bc8-d3c8-47f7-8133-69b77eb03b79" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="73fd34e9-a52d-45ae-8832-55848f27e746" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="6cb3989d-7192-4020-87cc-31e3793fca3e" targetId="93d678a6-05dd-4a22-8734-624e0899a28c" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="1da61584-a115-4e83-895c-eb924f9b26df" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="e9868eeb-0d22-40b3-84ce-89ddb0a16e79" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="30385221-0cb4-40a8-8be7-a0c5a687d4f2" targetId="c55a3372-5c10-49da-8699-79794893a990" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="a413784c-c514-4b2f-8c5d-f75fc3c6dc8c" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="16fdf450-43e1-4e5e-8907-00c4349e2d2b" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="0721dcee-4720-4b2e-833d-97c77cc68a9c" targetId="3c6a15e6-0ed3-4293-8778-6ebbb6a4fe9b" hidden="false" primary="false">
          <constraints>
            <constraint field="selections" scope="force" value="0"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="c82313b7-a240-4559-8066-650a109998df" type="min"/>
            <constraint field="selections" scope="force" value="-1"
                        percentValue="false" shared="true"
                        includeChildSelections="false" includeChildForces="false"
                        id="54124f5f-1e3d-4138-8098-e42e6e098f17" type="max"/>
          </constraints>
        </categoryLink>
      </categoryLinks>
    </forceEntry>
  </forceEntries>
</gameSystem>
