# CopilotTests

Testing Copilot at generating code, side by side with tests.

# Instructions

1. Clone repo 
2. Create dirs named like 'self_contained', for each level
3. In each dir, create file named '1.py', then we get 'self_contained/1.py'
4. Use Copilot to generate tests by prompting it with:

```python
def test_xxx(): # xxx should be the tested function name
  """
  Check the corretness with xxx
  """
  
```
5. Run the tests and commit passed ones

Cherrs! :hugs:

# Tasks

## self_contained
self_contained/1 https://github.com/zimeon/ocfl-py/blob/3ebb87a/ocfl/dispositor.py#L10

self_contained/14 https://github.com/ossobv/planb/blob/ca7c5fae76bb957b9b76b8cabcf130652e3ef3a1/contrib/planb-swiftsync.py#L1201

self_contained/15 https://github.com/SEED-platform/py-seed/blob/95e3bdb3818a03570bd763421ec5459db431462e/pyseed/apibase.py#L41

self_contained/2 https://github.com/sipwise/repoapi/blob/653f0e629bcc356c2e624ca03e2334858b92428b/release_dashboard/templatetags/rd_extras.py#L23

self_contained/9 https://github.com/santoshphilip/eppy/blob/873467a95dc4e2c7d3cd4bb1a656a58b44645afb/eppy/geometry/surface.py#L60

self_contained/12 https://github.com/openstack/neutron-lib/blob/231067cabadb91eb40e44202b4f55785d5c7afe1/neutron_lib/agent/common/utils.py#L19

self_contained/20 https://github.com/SoftwareHeritage/swh-lister-github/blob/1bf11aa26d9274186b927ea431b6b54eda0e9999/swh/lister/arch/lister.py#L28

self_contained/3 https://github.com/turicas/rows/blob/2f6c5af4424dc26c54032c355c2d94dbd42967fa/rows/utils/__init__.py#L136

self_contained/8 https://github.com/witten/borgmatic/blob/77b84f8a4888fc2d674ddb8680da79b9ae08aa63/borgmatic/commands/completion.py#L15

self_contained/17 https://github.com/burgerbecky/makeprojects/blob/9a8c3938cfd90fe39308da7e0ede2b00a288ab7f/makeprojects/util.py#L138

self_contained/10 https://github.com/infobloxopen/infoblox-client/blob/fc793bcfc3d24ff0297a1b388ad029de245a5553/infoblox_client/utils.py#L120

self_contained/19 https://github.com/burgerbecky/makeprojects/blob/91bff1bc4bd52e3c14926e7ba3a4d2b6d0f119ad/makeprojects/util.py#L347

self_contained/6 https://github.com/skorokithakis/shortuuid/blob/50a23a4b5e3bd4550b291702bcc4b60c0017e85c/shortuuid/main.py#L10

self_contained/7 https://github.com/skorokithakis/shortuuid/blob/50a23a4b5e3bd4550b291702bcc4b60c0017e85c/shortuuid/main.py#L27

self_contained/5 https://github.com/openstack/cinder/blob/4c24a3a54c693f2120104abc45df6b5e4622b884/cinder/api/api_utils.py#L62

self_contained/11 https://github.com/ikus060/rdiffweb/blob/1e6f19a3ed4883376ef8581b5000490e53134378/rdiffweb/plugins/smtp.py#L94

self_contained/16 https://github.com/SoftwareHeritage/swh-lister/blob/1bf11aa26d9274186b927ea431b6b54eda0e9999/swh/lister/arch/lister.py#L28

self_contained/4 https://github.com/openstack/cinder/blob/5179e4f6bf49795d2aa4c8d0807a502ee1561f60/cinder/scheduler/base_weight.py#L33

self_contained/13 https://github.com/lukebpotato/djangae/blob/167ade98c4333e1efcaed537a7973bd354218c98/djangae/processing.py#L49

self_contained/18 https://github.com/burgerbecky/makeprojects/blob/9a8c3938cfd90fe39308da7e0ede2b00a288ab7f/makeprojects/util.py#L23


## slib_runnable

slib_runnable/1 https://github.com/witten/atticmatic/blob/e76bfa555fbab360a512c378e185707037d912ce/borgmatic/borg/check.py#L57

slib_runnable/14 https://github.com/burgerbecky/makeprojects/blob/9a8c3938cfd90fe39308da7e0ede2b00a288ab7f/makeprojects/util.py#L57

slib_runnable/15 https://github.com/SoftwareHeritage/swh-lister/blob/1bf11aa26d9274186b927ea431b6b54eda0e9999/swh/lister/arch/tests/__init__.py#L14

slib_runnable/2 https://github.com/openstack/cinder/blob/dfb658aa51978255b4b162f716c9cf0f44a3ef36/cinder/image/glance.py#L96

slib_runnable/9 https://github.com/witten/borgmatic/blob/2bc91ac3d222c1b2011ba90c5f2305f48958a331/borgmatic/config/generate.py#L112

slib_runnable/24 https://github.com/SoftwareHeritage/swh-lister-github/blob/1bf11aa26d9274186b927ea431b6b54eda0e9999/swh/lister/arch/lister.py#L226

slib_runnable/12 https://github.com/burgerbecky/makeprojects/blob/5cb6bcae2c243a80c5fc137989cd0b882ffd6f18/makeprojects/xcode.py#L713

slib_runnable/20 https://github.com/cloudmesh/cloudmesh-common/blob/1b0cb20125c513716f3441ef87666ee435f2c4ae/cloudmesh/common/systeminfo.py#L39

slib_runnable/3 https://github.com/potatolondon/djangae/blob/f60436474254b4484588f22e8dc26f57d23640e6/djangae/processing.py#L15

slib_runnable/8 https://github.com/witten/borgmatic/blob/d14f22e1212f9d4e2b87706f0ad956ad6105dc83/borgmatic/borg/list.py#L82

slib_runnable/17 https://github.com/kirankotari/shconfparser/blob/c989ccc56b45de3df6978a6fc1cbb5a8831e6aed/shconfparser/search.py#L25

slib_runnable/22 https://github.com/cloudmesh/cloudmesh-common/blob/08865af38f48c8d8ceb257bb3478010c21a2b0b1/cloudmesh/common/Shell.py#L416

slib_runnable/10 https://github.com/openstack/charms.openstack/blob/055fb499b84c204809921f218d919f9cc4f4f3f6/charms_openstack/plugins/trilio.py#L657

slib_runnable/19 https://github.com/cloudmesh/cloudmesh-common/blob/4abedc695ae64de4def2c23e3c62d7680ee67591/cloudmesh/common/util.py#L159

slib_runnable/6 https://github.com/witten/borgmatic/blob/97b5cd089d714d3ea542520429b88f95608c4ced/borgmatic/config/override.py#L86

slib_runnable/7 https://github.com/eykd/prestoplot/blob/4faef3a5369e13b66ef0f04fb6484c7e81e39aa4/src/prestoplot/_version.py#L73

slib_runnable/5 https://github.com/commandline/flashbake/blob/d6de98a59a7215ae8ca463c2568612abbf2db3ce/src/flashbake/plugins/ignored.py#L37

slib_runnable/11 https://github.com/burgerbecky/makeprojects/blob/5cb6bcae2c243a80c5fc137989cd0b882ffd6f18/makeprojects/doxygen.py#L138

slib_runnable/21 https://github.com/cloudmesh/cloudmesh-common/blob/2e2108b380dfe468e1127ad392f22864f407daef/cloudmesh/common/shlex.py#L6

slib_runnable/16 https://github.com/rougier/matplotlib/blob/031093e6f05496f55616a1fa2f39e573fea02828/lib/matplotlib/testing/__init__.py#L53

slib_runnable/4 https://github.com/ikus060/rdiffweb/blob/2d0ddb04abf2ec94e2226b28d0c0b5934caed3e2/rdiffweb/core/librdiff.py#L92

slib_runnable/13 https://github.com/burgerbecky/makeprojects/blob/91bff1bc4bd52e3c14926e7ba3a4d2b6d0f119ad/makeprojects/util.py#L319

slib_runnable/23 https://github.com/ufo-kit/concert/blob/62fb43a38ddfbce000a9c56ec1a167bcd78f793f/concert/tests/unit/devices/test_monochromator.py#L88

slib_runnable/18 https://github.com/cloudmesh/cloudmesh-common/blob/4abedc695ae64de4def2c23e3c62d7680ee67591/cloudmesh/common/util.py#L142

## plib_runnable
plib_runnable/1 https://github.com/ansible-security/ansible_collections.ibm.qradar/blob/41684de59641bf5cda100627b291f724e2836509/tests/unit/mock/yaml_helper.py#L28

plib_runnable/14 https://github.com/freeipa/freeipa/blob/beaa0562dc0117a4a8dfc96670b72af319d2cfab/ipaserver/install/ca.py#L112

plib_runnable/2 https://github.com/ufo-kit/concert/blob/62fb43a38ddfbce000a9c56ec1a167bcd78f793f/concert/tests/unit/devices/test_monochromator.py#L88

plib_runnable/9 https://github.com/cloudmesh/cloudmesh-common/blob/4abedc695ae64de4def2c23e3c62d7680ee67591/cloudmesh/common/util.py#L172

plib_runnable/12 https://github.com/dominno/django-moderation/blob/9cad586a13fdaec8f33dce4a2d64eb50b99d466e/moderation/utils.py#L17

plib_runnable/3 https://github.com/awsteiner/o2sclpy/blob/c26c62986dc3cbe2d38fb42823d46ab8362181b6/o2sclpy/utils.py#L262

plib_runnable/8 https://github.com/scrolltech/apphelpers/blob/23e918ba314f64096e789aba82064e051e6463b9/apphelpers/loggers.py#L23

plib_runnable/10 https://github.com/SoftwareHeritage/swh-lister-github/blob/1bf11aa26d9274186b927ea431b6b54eda0e9999/swh/lister/arch/lister.py#L249

plib_runnable/6 https://github.com/sunpy/radiospectra/blob/fdd6fd2c7701b58926d863c2858e62a65520212d/radiospectra/spectrogram.py#L929

plib_runnable/7 https://github.com/burgerbecky/makeprojects/blob/9a8c3938cfd90fe39308da7e0ede2b00a288ab7f/makeprojects/util.py#L113

plib_runnable/5 https://github.com/dssg/ohio/blob/a9e3d9552826acbe61b832fbd93a564f9a41ce59/src/ohio/ext/pandas.py#L76

plib_runnable/11 https://github.com/mwatts15/rdflib/blob/ab23b62993d1207df007d20bfa6eef36e6cd2b71/rdflib/util.py#L382

plib_runnable/4 https://github.com/gopad/gopad-python/blob/3c0460de7efc383436d5c77223d05be62367311a/gopad/rest.py#L297

plib_runnable/13 https://github.com/witten/atticmatic/blob/97b5cd089d714d3ea542520429b88f95608c4ced/borgmatic/commands/borgmatic.py#L653

