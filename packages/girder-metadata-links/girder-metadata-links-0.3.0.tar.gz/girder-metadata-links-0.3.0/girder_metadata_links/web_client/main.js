import { wrap } from '@girder/core/utilities/PluginUtils';
import MetadataWidget from '@girder/core/views/widgets/MetadataWidget';
import Folder from '@girder/core/models/FolderModel';
import Item from '@girder/core/models/ItemModel';
import template from './link.pug';

wrap(MetadataWidget, 'render', function (render) {
   render.call(this);

   this.$('.g-widget-metadata-value').each((i, el) => {
       [Folder, Item].forEach(type => {
           const rname = type.prototype.resourceName;
           if (el.innerHTML.startsWith(`girder:${rname}:`)) {
               const id = el.innerHTML.substring(8 + rname.length);
               const model = new type({_id: id});
               model.fetch({ignoreError: true}).done(() => {
                   el.innerHTML = template({
                       id,
                       rname,
                       name: model.name()
                   });
               });
           }
       });
   });
});
