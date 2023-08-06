## pymania
A minimalistic server controller for the popular Trackmania racing games.

### Features
- Centralized configuration for all plugins
- Already contains plugins for out-of-the-box use
- Ability to reload configuration and plugin code during execution
- Asynchronous/parallel plugin loading (order and parallelism determined from inter-dependencies)
- Dedicated server handler ID allocation does not create overlaps and is therefore suitable for high-load environments
- Completely dynamic and fine-grained control over privileges
- Scalable to a certain extent, despite dedicated server limitations
