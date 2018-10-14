var aws = require('aws-sdk');  
aws.config.region = 'ap-southeast-1';  
var ec2 = new aws.EC2();  
var d = new Date();  
var x = 7;  /* ------Retention Days------- */  
d.setDate(d.getDate() - x);  
reqdate = d.toISOString().substring(0, 10);  
exports.handler = function(event, context) {  
    ec2.describeImages({
        Owners: [
            'self'
        ],
        Filters: [{
            Name: 'tag:DeleteOn',
            Values: [
                'yes'
            ]
        }]

    }, function(err, data) {
        if (err) console.log(err, err.stack);
        else {
            for (var j in data.Images) {
                imagename = data.Images[j].Name
                imageid = data.Images[j].ImageId

                if (imagename.indexOf(reqdate) > -1) {
                    console.log("image that is going to be deregistered: ", imagename);
                    console.log("image id: ", imageid);

                    var deregisterparams = {
                        ImageId: imageid
                    };
                    ec2.deregisterImage(deregisterparams, function(err, data01) {
                        if (err) console.log(err, err.stack); // an error occurred
                        else {
                            console.log("Image Deregistered");
                        }
                    });
                }
            }
            setTimeout(function() {
                for (var j in data.Images) {
                    imagename = data.Images[j].Name
                    if (imagename.indexOf(reqdate) > -1) {
                        for (var k in data.Images[j].BlockDeviceMappings) {
                            snap = data.Images[j].BlockDeviceMappings[k].Ebs.SnapshotId;
                            console.log(snap);
                            var snapparams = {
                                SnapshotId: snap
                            };
                            ec2.deleteSnapshot(snapparams, function(err, data) {
                                if (err) console.log(err, err.stack); // an error occurred
                                else console.log("Snapshot Deleted"); // successful response
                            });
                        }
                    }
                }
            }, 10000);
        }
    });
}